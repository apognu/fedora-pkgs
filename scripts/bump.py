#!/usr/bin/env python3
"""
Check upstream for new versions and update the specs accordingly.

Packages with a new upstream version get their Version (or commit) updated
and their Release reset to 1. Packages depending on them, transitively, get
their Release bumped so they are rebuilt against the new version.

The list of packages to build is printed on stdout, and written to
$GITHUB_OUTPUT as `packages` when running in GitHub Actions.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "specs"
NEWVER = ROOT / ".nvchecker" / "newver.json"

RE_VERSION = re.compile(r"^(Version:\s*)(\S+)$", re.M)
RE_RELEASE = re.compile(r"^(Release:\s*)(\d+)(%\{\?dist\})$", re.M)
RE_COMMIT = re.compile(r"^(%global\s+commit\s+)([0-9a-f]{40})$", re.M)
RE_COMMITDATE = re.compile(r"^(%global\s+commitdate\s+)(\d{8})$", re.M)


def log(*args):
    print(*args, file=sys.stderr)


def load_packages():
    with open(ROOT / "packages.toml", "rb") as f:
        return {name: conf.get("deps", []) for name, conf in tomllib.load(f).items()}


def spec_path(pkg):
    return SPECS / pkg / f"{pkg}.spec"


def current_version(spec):
    if m := RE_COMMIT.search(spec):
        return m.group(2)

    return RE_VERSION.search(spec).group(2)


def run_nvchecker():
    NEWVER.parent.mkdir(exist_ok=True)
    NEWVER.unlink(missing_ok=True)

    subprocess.run(["nvchecker", "-c", str(ROOT / "nvchecker.toml")], cwd=ROOT, check=True)

    with open(NEWVER) as f:
        data = json.load(f)

    return data.get("data", {})


def upstream_version(entry, spec):
    if RE_COMMIT.search(spec):
        return entry.get("revision")

    return entry.get("version")


def update_version(spec, entry):
    if RE_COMMIT.search(spec):
        spec = RE_COMMIT.sub(lambda m: m.group(1) + entry["revision"], spec)
        spec = RE_COMMITDATE.sub(lambda m: m.group(1) + entry["version"][:8], spec)
    else:
        spec = RE_VERSION.sub(lambda m: m.group(1) + entry["version"], spec)

    return RE_RELEASE.sub(lambda m: f"{m.group(1)}1{m.group(3)}", spec)


def bump_release(spec):
    return RE_RELEASE.sub(lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}", spec)


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
        old = current_version(spec)

        if new is None or new == old:
            continue

        if "-" in entry["version"]:
            log(f"warning: {pkg} {entry['version']} is not a valid RPM version, skipping")
            continue

        log(f"{pkg}: {old} -> {new}")
        changed[pkg] = entry

    rebuilds = reverse_deps(packages, changed)

    for pkg in sorted(rebuilds):
        log(f"{pkg}: rebuild (dependency updated)")

    if not args.dry_run:
        for pkg, entry in changed.items():
            path = spec_path(pkg)
            path.write_text(update_version(path.read_text(), entry))

        for pkg in rebuilds:
            path = spec_path(pkg)
            path.write_text(bump_release(path.read_text()))

    # Keep the order of packages.toml, which is a valid build order
    result = [pkg for pkg in packages if pkg in changed or pkg in rebuilds]
    print(" ".join(result))

    if output := os.environ.get("GITHUB_OUTPUT"):
        with open(output, "a") as f:
            f.write(f"packages={' '.join(result)}\n")


if __name__ == "__main__":
    main()
