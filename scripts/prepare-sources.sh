#!/usr/bin/env bash
# Download remote sources of a spec and run its optional prepare hook.
#
# Usage: prepare-sources.sh <spec> <sourcedir>
#
# A package may ship a `prepare.sh` next to its spec to generate extra
# sources (e.g. vendored crates). It is called with the spec path and
# the source directory.

set -euo pipefail

SPEC="$1"
SOURCEDIR="$2"

spectool -g -C "$SOURCEDIR" "$SPEC"

if [[ -x "$SOURCEDIR/prepare.sh" ]]; then
  "$SOURCEDIR/prepare.sh" "$SPEC" "$SOURCEDIR"
fi
