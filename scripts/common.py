"""Helpers shared by the build and bump scripts."""

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "specs"

# Supported Fedora releases. Keep in sync with the `release` input of
# .github/workflows/update.yml.
RELEASES = [44, 45]


def log(*args):
    print(*args, file=sys.stderr, flush=True)


def load_config():
    with open(ROOT / "packages.toml", "rb") as f:
        return tomllib.load(f)


def load_packages():
    return {name: conf.get("deps", []) for name, conf in load_config().items()}


def load_releases():
    """Fedora releases each package is built for (all supported by default)."""

    result = {}

    for name, conf in load_config().items():
        releases = conf.get("releases", RELEASES)

        if unknown := set(releases) - set(RELEASES):
            raise ValueError(f"{name}: unsupported releases {sorted(unknown)}")

        result[name] = releases

    return result


def spec_path(pkg):
    return SPECS / pkg / f"{pkg}.spec"
