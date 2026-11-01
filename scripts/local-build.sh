#!/usr/bin/env bash
# Build one or more packages locally inside a Fedora container.
#
# Previously built RPMs are exposed to later builds through a local
# repository, so packages can be built in dependency order:
#
#   scripts/local-build.sh hyprutils hyprlang

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${OUT:-/tmp/copr-out}"
IMAGE="${IMAGE:-registry.fedoraproject.org/fedora:44}"

mkdir -p "$OUT/repo" "$OUT/cache"

for pkg in "$@"; do
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
