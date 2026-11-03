#!/usr/bin/env bash
# Build one or more packages locally inside a Fedora container.
#
# Packages are built in dependency order, and previously built RPMs are
# exposed to later builds through a local repository. Dependencies are not
# added automatically: they must be listed or already built in $OUT.
#
# $FEDORA selects the Fedora release (default: 44). Packages that do not
# target that release are left out.
#
#   scripts/local-build.sh hyprlang hyprutils
#   FEDORA=45 scripts/local-build.sh all

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FEDORA="${FEDORA:-44}"
OUT="${OUT:-/tmp/copr-out/$FEDORA}"
IMAGE="${IMAGE:-registry.fedoraproject.org/fedora:$FEDORA}"

read -ra PACKAGES <<< "$(python3 "$ROOT/scripts/build.py" --order --release "$FEDORA" "$@")"

mkdir -p "$OUT/repo" "$OUT/cache"

for pkg in "${PACKAGES[@]}"; do
  echo ">>> building $pkg"

  podman run --rm \
    -v "$ROOT:/src:ro,z" \
    -v "$OUT:/out:z" \
    -v "$OUT/cache:/var/cache/libdnf5:z" \
    "$IMAGE" \
    bash -euxo pipefail -c "
      echo keepcache=True >> /etc/dnf/dnf.conf

      dnf -y -q install rpm-build rpmdevtools createrepo_c 'dnf5-command(builddep)' cargo

      createrepo_c -q /out/repo

      cat > /etc/yum.repos.d/local.repo <<EOF
[local]
name=local
baseurl=file:///out/repo
gpgcheck=0
priority=1
EOF

      mkdir -p ~/rpmbuild/SOURCES
      cp -r /src/specs/$pkg/. ~/rpmbuild/SOURCES/

      /src/scripts/prepare-sources.sh ~/rpmbuild/SOURCES/$pkg.spec ~/rpmbuild/SOURCES

      dnf -y -q builddep --refresh ~/rpmbuild/SOURCES/$pkg.spec

      rpmbuild -ba ~/rpmbuild/SOURCES/$pkg.spec

      find ~/rpmbuild/RPMS -name '*.rpm' ! -name '*debug*' -exec cp {} /out/repo/ \;
      cp ~/rpmbuild/SRPMS/*.src.rpm /out/
    "
done
