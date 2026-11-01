#!/usr/bin/env bash
# Vendor the Rust crates so the build can run offline on COPR.
#
# Usage: prepare.sh <spec> <sourcedir>

set -euo pipefail

SPEC="$1"
SOURCEDIR="$2"

VERSION="$(rpmspec -q --srpm --qf '%{version}' "$SPEC")"
VENDOR="$SOURCEDIR/swayosd-$VERSION-vendor.tar.gz"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

tar xf "$SOURCEDIR/swayosd-$VERSION.tar.gz" -C "$WORK"

cd "$WORK/SwayOSD-$VERSION"
rm -f rust-toolchain.toml
cargo vendor --locked vendor > /dev/null

tar czf "$VENDOR" vendor
