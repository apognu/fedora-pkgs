#!/usr/bin/env python3
"""
Check upstream for new versions and update the specs accordingly.

Packages with a new upstream version get their Version (or commit) updated
and their Release reset to 1. Packages depending on them, transitively, get
their Release bumped so they are rebuilt against the new version.

Every updated spec is checked to produce a greater version-release than the
current one, so that the new packages always upgrade the installed ones.

The list of packages to build is printed on stdout, and written to
$GITHUB_OUTPUT as `packages` when running in GitHub Actions.
"""

import argparse
import json
import os
import re
import subprocess
import tempfile

from common import ROOT, load_packages, log, spec_path

NEWVER = ROOT / ".nvchecker" / "newver.json"

# All patterns capture the text preceding the value, then the value itself
RE_VERSION = re.compile(r"^(Version:\s*)(\S+)$", re.M)
RE_RELEASE = re.compile(r"^(Release:\s*)(\d+)(?=%\{\?dist\}$)", re.M)
RE_COMMIT = re.compile(r"^(%global\s+commit\s+)([0-9a-f]{40})$", re.M)
RE_COMMITDATE = re.compile(r"^(%global\s+commitdate\s+)(\d{8}\.\d{6})$", re.M)

# Release versions only: pre-releases (1.0-rc1, 1.0.beta2...) are skipped,
# since they would not compare as expected against the final release.
RE_VALID_VERSION = re.compile(r"^[0-9][0-9.]*[a-z]?$")

# nvchecker reports the date of the latest commit of git sources as
# YYYYMMDD.HHMMSS, which keeps snapshot versions ordered.
RE_VALID_COMMITDATE = re.compile(r"^\d{8}\.\d{6}$")


def find(pkg, regex, spec):
    if m := regex.search(spec):
        return m.group(2)

    raise RuntimeError(f"{pkg}: no match for {regex.pattern!r} in spec")


def replace(pkg, regex, spec, value):
    # Only the first match is replaced: the preamble comes first, other
    # matches may be anywhere else (e.g. a Version: line in a heredoc).
    spec, count = regex.subn(lambda m: m.group(1) + value, spec, count=1)

    if count != 1:
        raise RuntimeError(f"{pkg}: no match for {regex.pattern!r} in spec")

    return spec


def is_snapshot(spec):
    return RE_COMMIT.search(spec) is not None


def current_version(pkg, spec):
    if is_snapshot(spec):
        return find(pkg, RE_COMMIT, spec)

    return find(pkg, RE_VERSION, spec)


def upstream_version(entry, spec):
    if is_snapshot(spec):
        return entry.get("revision")

    return entry.get("version")


def valid_version(entry, spec):
    if is_snapshot(spec):
        return RE_VALID_COMMITDATE.match(entry["version"]) is not None

    return RE_VALID_VERSION.match(entry["version"]) is not None


def update_version(pkg, spec, entry):
    if is_snapshot(spec):
        spec = replace(pkg, RE_COMMIT, spec, entry["revision"])
        spec = replace(pkg, RE_COMMITDATE, spec, entry["version"])
    else:
        spec = replace(pkg, RE_VERSION, spec, entry["version"])

    return replace(pkg, RE_RELEASE, spec, "1")


def bump_release(pkg, spec):
    release = int(find(pkg, RE_RELEASE, spec))

    return replace(pkg, RE_RELEASE, spec, str(release + 1))


def rpm_evr(path):
    proc = subprocess.run(
        ["rpmspec", "-q", "--srpm", "--qf", "%{evr}", path],
        check=True,
        capture_output=True,
        text=True,
    )

    return proc.stdout.strip()


def ensure_newer(pkg, spec):
    old = rpm_evr(spec_path(pkg))

    with tempfile.NamedTemporaryFile("w", suffix=".spec") as f:
        f.write(spec)
        f.flush()

        new = rpm_evr(f.name)

    # rpmdev-vercmp exits with 12 when the second version is newer
    if subprocess.run(["rpmdev-vercmp", old, new], stdout=subprocess.DEVNULL).returncode != 12:
        raise RuntimeError(f"{pkg}: new version {new} is not greater than {old}")

    return old, new


def run_nvchecker():
    NEWVER.parent.mkdir(exist_ok=True)
    NEWVER.unlink(missing_ok=True)

    subprocess.run(["nvchecker", "-c", str(ROOT / "nvchecker.toml")], cwd=ROOT, check=True)

    with open(NEWVER) as f:
        data = json.load(f)

    return data.get("data", {})


def reverse_deps(packages, changed):
    rdeps = set()
    queue = list(changed)

    while queue:
        pkg = queue.pop()

        for name, deps in packages.items():
            if pkg in deps and name not in rdeps and name not in changed:
                rdeps.add(name)
                queue.append(name)

    return rdeps


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="do not modify the specs")
    args = parser.parse_args()

    packages = load_packages()
    upstream = run_nvchecker()

    changed = {}

    for pkg in packages:
        spec = spec_path(pkg).read_text()
        entry = upstream.get(pkg)

        if not entry:
            log(f"warning: no upstream version found for {pkg}")
            continue

        new = upstream_version(entry, spec)
        old = current_version(pkg, spec)

        if new is None or new == old:
            continue

        if not valid_version(entry, spec):
            log(f"warning: {pkg} {entry['version']} is not a release version, skipping")
            continue

        changed[pkg] = entry

    rebuilds = reverse_deps(packages, changed)
    updates = {}

    for pkg, entry in changed.items():
        updates[pkg] = update_version(pkg, spec_path(pkg).read_text(), entry)

    for pkg in rebuilds:
        updates[pkg] = bump_release(pkg, spec_path(pkg).read_text())

    # Keep the order of packages.toml, which is a valid build order
    result = [pkg for pkg in packages if pkg in updates]

    for pkg in result:
        old, new = ensure_newer(pkg, updates[pkg])
        reason = "" if pkg in changed else " (dependency updated)"

        log(f"{pkg}: {old} -> {new}{reason}")

    if not args.dry_run:
        for pkg, spec in updates.items():
            spec_path(pkg).write_text(spec)

    print(" ".join(result))

    if output := os.environ.get("GITHUB_OUTPUT"):
        with open(output, "a") as f:
            f.write(f"packages={' '.join(result)}\n")


if __name__ == "__main__":
    main()
