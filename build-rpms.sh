#!/bin/bash
# Build the giapi-glue-cc and gmp-server RPMs from the tarballs in SOURCES/.
#
#   ./build-rpms.sh            # RPMs (and SRPMs) land in rpms/
#
# The tarballs are not in git (each exceeds GitHub's file size limit); put them
# in SOURCES/ first. Their checksums are checked against SHA256SUMS before
# anything is built. Builds in a clean rockylinux:9 container, so the RPMs are
# .el9 whatever this machine runs.
set -euo pipefail
cd "$(dirname "$0")"
sha256sum --check --strict SHA256SUMS
mkdir -p rpms
docker run --rm --platform linux/amd64 \
    -v "$PWD":/src:ro -v "$PWD/rpms":/out \
    -e OWNER="$(id -u):$(id -g)" \
    rockylinux:9 bash -euo pipefail -c '
        dnf -q -y install rpm-build libxcrypt-compat >/dev/null
        mkdir -p ~/rpmbuild/SOURCES
        cp /src/SOURCES/*.tar.gz ~/rpmbuild/SOURCES/
        for spec in /src/*.spec; do rpmbuild -ba --quiet "$spec"; done
        cp ~/rpmbuild/RPMS/*/*.rpm ~/rpmbuild/SRPMS/*.rpm /out/
        chown -R "$OWNER" /out
    '
ls -l rpms/
