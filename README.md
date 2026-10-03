# gnirsdc-giapi-gmp

Prebuilt libraries the GNIRS detector controller uses that are **built by
another Gemini team**, kept here as versioned, checksummed release assets and
republished as an image for the GNIRS DC build to copy from.

They used to be committed to `gnirsdc-data-manager` as tarballs. GitHub rejects
files over 100 MB, and git history is a poor place for binaries anyway; this
repo keeps the same guarantees -- every version retrievable, every change
attributable -- without putting the binaries in git.

## What is here

| release tag | asset | unpacks to | what it is |
|---|---|---|---|
| `giapi-glue-cc-rocky8-2024.04` | `giapi-gluecc_rocky8.tar.gz` | `/giapi-glue-cc` | GIAPI C++ glue library, the instrument side of the Gemini Master Process interface, as a Rocky 8 build tree: source, `install/` (`libgiapi-glue-cc.so`) and its `external/` dependencies (activemq-cpp, log4cxx, apr, curl/curlpp, boost), each with its built libraries. Loaded by the DC through cppyy. |
| `gmp-server-0.2.6` | `gmp-server-0.2.6-SNAPSHOT.tar.gz` | `/gmp-server-0.2.6-SNAPSHOT` | Gemini Master Process server distribution (Java/OSGi, from the ASPEN repository): ActiveMQ broker, GDS keyword collection, GIAPI services. |

Both were committed to `gnirsdc-data-manager` on GitLab, where their history
remains: GMP in `14cee43` (2024-01-18), GIAPI in `246b607` (2024-04-24).

`RELEASES` is the source of truth: release tag, file name and SHA-256 of each
asset. The Releases page is where to download them by hand.

## Using it

Pin a published `VERSION` and copy what you need:

```dockerfile
COPY --from=ghcr.io/gemini-rtsw/gnirsdc-giapi-gmp:1.0.0 /giapi-glue-cc /gnirsdc/giapi-glue-cc
COPY --from=ghcr.io/gemini-rtsw/gnirsdc-giapi-gmp:1.0.0 /gmp-server-0.2.6-SNAPSHOT /gmp-server
```

The image is built `FROM scratch` and holds only the unpacked trees -- it is a
source for `COPY --from`, not something to run. A repo that builds from it needs
read access to this package (package settings → Manage Actions access).

Every image is also tagged `git-<sha>` for the commit that built it.

## Adding or replacing a tarball

1. Create a release with a new tag and attach the tarball. Never re-upload over
   an existing asset: the tag is the version.
   ```bash
   gh release create giapi-glue-cc-rocky8-2026.10 giapi-gluecc_rocky8.tar.gz \
       --repo gemini-rtsw/gnirsdc-giapi-gmp --title "GIAPI glue, Rocky 8, 2026-10" \
       --notes "Built from <source repo> <commit> by <who>; replaces 2024.04 because ..."
   ```
2. Update its line in `RELEASES` (tag, file name, `sha256sum` output) and bump
   `VERSION`.
3. Open a PR. CI downloads the assets, verifies the checksums and builds the
   image without pushing; merging publishes `ghcr.io/gemini-rtsw/gnirsdc-giapi-gmp:<VERSION>`.
4. Move consumers to the new `VERSION`.

A published `VERSION` is never overwritten: changing `RELEASES` or the
`Dockerfile` without bumping it fails the publish, so an existing pin always
gets the image it was tested with.

## Building locally

```bash
./fetch-assets.sh        # downloads with gh, or just verifies files you put in assets/
docker build --platform linux/amd64 -t gnirsdc-giapi-gmp:local .
```
