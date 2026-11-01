#!/usr/bin/env python3
"""
Build source RPMs and submit them to COPR, layer by layer.

Packages are grouped in layers following the dependency graph from
packages.toml: each layer is submitted at once and waited for before the
next one starts, so that packages are built against freshly built
dependencies. Packages whose dependencies failed are skipped.

A Markdown report is written to --report, if given.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from common import ROOT, SPECS, load_packages, log

DEFAULT_PROJECT = os.environ.get("COPR_PROJECT", "apognu/fedora-pkgs")


def all_deps(packages, pkg):
    seen = set()
    queue = list(packages[pkg])

    while queue:
        dep = queue.pop()

        if dep not in seen:
            seen.add(dep)
            queue.extend(packages[dep])

    return seen


def layers(packages, selected):
    remaining = set(selected)
    result = []

    while remaining:
        layer = [
            pkg for pkg in packages
            if pkg in remaining and not (all_deps(packages, pkg) & remaining)
        ]

        if not layer:
            raise RuntimeError(f"dependency cycle among {sorted(remaining)}")

        result.append(layer)
        remaining -= set(layer)

    return result


def build_srpm(pkg, workdir):
    sourcedir = workdir / pkg / "sources"
    srpmdir = workdir / pkg / "srpm"

    shutil.copytree(SPECS / pkg, sourcedir)

    spec = sourcedir / f"{pkg}.spec"

    subprocess.run([ROOT / "scripts" / "prepare-sources.sh", spec, sourcedir], check=True)

    subprocess.run(
        [
            "rpmbuild", "-bs", spec,
            "--define", f"_sourcedir {sourcedir}",
            "--define", f"_srcrpmdir {srpmdir}",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )

    srpms = list(srpmdir.glob("*.src.rpm"))

    if len(srpms) != 1:
        raise RuntimeError(f"expected one SRPM for {pkg}, found {srpms}")

    return srpms[0]


def submit(project, srpm):
    proc = subprocess.run(
        ["copr-cli", "build", "--nowait", project, srpm],
        check=True,
        capture_output=True,
        text=True,
    )

    if m := re.search(r"Created builds: (\d+)", proc.stdout):
        return int(m.group(1))

    raise RuntimeError(f"could not find build ID in copr-cli output:\n{proc.stdout}")


def build_status(build_id):
    proc = subprocess.run(["copr-cli", "status", str(build_id)], capture_output=True, text=True)

    return proc.stdout.strip() or "unknown"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("packages", nargs="*", help="packages to build, or `all` (default: all)")
    parser.add_argument("--project", default=DEFAULT_PROJECT, help=f"COPR project (default: {DEFAULT_PROJECT})")
    parser.add_argument("--report", type=Path, help="write a Markdown report to this file")
    parser.add_argument("--dry-run", action="store_true", help="print the build plan and exit")
    parser.add_argument("--order", action="store_true", help="print the packages in build order and exit")
    args = parser.parse_args()

    packages = load_packages()
    selected = args.packages or ["all"]

    if selected == ["all"]:
        selected = list(packages)

    if unknown := [pkg for pkg in selected if pkg not in packages]:
        sys.exit(f"unknown packages: {' '.join(unknown)}")

    plan = layers(packages, selected)

    if args.order:
        print(" ".join(pkg for layer in plan for pkg in layer))
        return

    for i, layer in enumerate(plan, 1):
        log(f"layer {i}: {' '.join(layer)}")

    if args.dry_run:
        return

    results = {}
    failed = set()
    url = f"https://copr.fedorainfracloud.org/coprs/{args.project}/build"

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)

        for i, layer in enumerate(plan, 1):
            builds = {}

            for pkg in layer:
                if broken := all_deps(packages, pkg) & failed:
                    log(f"{pkg}: skipped, dependencies failed: {' '.join(sorted(broken))}")
                    results[pkg] = ("skipped", None)
                    failed.add(pkg)
                    continue

                try:
                    srpm = build_srpm(pkg, workdir)
                    builds[pkg] = submit(args.project, srpm)
                    log(f"{pkg}: submitted {url}/{builds[pkg]}/")
                except (subprocess.CalledProcessError, RuntimeError) as e:
                    log(f"{pkg}: SRPM or submission failed: {e}")

                    if output := (getattr(e, "stderr", None) or getattr(e, "stdout", None) or "").strip():
                        log(output)

                    results[pkg] = ("srpm-failed", None)
                    failed.add(pkg)

            if builds:
                log(f"layer {i}: waiting for {len(builds)} builds")
                subprocess.run(["copr-cli", "watch-build", *map(str, builds.values())])

            for pkg, build_id in builds.items():
                status = build_status(build_id)
                results[pkg] = (status, build_id)

                if status != "succeeded":
                    failed.add(pkg)

    lines = ["| Package | Status | Build |", "|---|---|---|"]

    for pkg in selected:
        status, build_id = results.get(pkg, ("not run", None))
        link = f"[{build_id}]({url}/{build_id}/)" if build_id else ""
        lines.append(f"| {pkg} | {status} | {link} |")

    report = "\n".join(lines)
    log(report)

    if args.report:
        args.report.write_text(report + "\n")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
