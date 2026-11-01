"""Helpers shared by the build and bump scripts."""

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "specs"


def log(*args):
    print(*args, file=sys.stderr, flush=True)


def load_packages():
    with open(ROOT / "packages.toml", "rb") as f:
        return {name: conf.get("deps", []) for name, conf in tomllib.load(f).items()}


def spec_path(pkg):
    return SPECS / pkg / f"{pkg}.spec"
