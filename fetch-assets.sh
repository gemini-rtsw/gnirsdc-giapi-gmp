#!/bin/bash
# Download every asset listed in RELEASES into assets/ and verify it.
#
#   ./fetch-assets.sh
#
# A file already in assets/ is not downloaded again, only verified -- so for a
# local build you can drop the tarballs there yourself. Downloading needs the
# gh CLI, logged in (CI sets GH_TOKEN).
#
# Fails if a checksum differs from RELEASES, or if assets/ holds a tarball that
# RELEASES does not list: the Dockerfile unpacks every assets/*.tar.gz, so an
# unlisted file would end up in the image unverified.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets

listed=()
while read -r tag file sum; do
    case "$tag" in ''|\#*) continue ;; esac
    listed+=("$file")
    if [ ! -f "assets/$file" ]; then
        echo "Downloading $file from release $tag"
        gh release download "$tag" --pattern "$file" --dir assets
    fi
    echo "$sum  assets/$file" | sha256sum --check --strict
done < RELEASES

for f in assets/*.tar.gz; do
    [ -e "$f" ] || continue
    name=$(basename "$f")
    if ! printf '%s\n' "${listed[@]}" | grep -qxF "$name"; then
        echo "ERROR: $f is not listed in RELEASES; remove it or add it there." >&2
        exit 1
    fi
done
