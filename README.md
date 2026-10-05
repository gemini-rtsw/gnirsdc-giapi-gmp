# gnirsdc-giapi-gmp

Packaging for two libraries the GNIRS detector controller uses that are
**built by another Gemini team**: the GIAPI C++ glue and the GMP server. They
are packaged as RPMs from the prebuilt tarballs and registered in the shared
gemini-rtsw rpm-repo by hand, the way resources we do not build ourselves are.
`gnirsdc-data-manager` pins both in its spec.

| RPM | from | installs | what it is |
|---|---|---|---|
| `giapi-glue-cc-0.16-1.el9.x86_64` | `giapi-gluecc_rocky8.tar.gz` | `/opt/giapi-glue-cc` | GIAPI C++ glue library, the instrument side of the Gemini Master Process interface, as its Rocky 8 build tree: source, `install/` (`libgiapi-glue-cc.so`) and `external/` (activemq-cpp, log4cxx, apr, curl/curlpp, boost) with their built libraries. Requires `libxcrypt-compat` on EL9. Loaded by the DC through cppyy. |
| `gmp-server-0.2.6-0.1.SNAPSHOT.el9.noarch` | `gmp-server-0.2.6-SNAPSHOT.tar.gz` | `/opt/gmp-server` | Gemini Master Process server distribution (Java/OSGi, from the ASPEN repository): ActiveMQ broker, GDS keyword collection, GIAPI services. Requires Java 8. |

Both tarballs were committed to `gnirsdc-data-manager` on GitLab, where their
history remains: GMP in `14cee43` (2024-01-18), GIAPI in `246b607`
(2024-04-24).

## Why by hand

The tarballs are not in git: each is larger than GitHub's 100 MB file limit.
What is versioned and backed up is:

- **this repo** -- the specs, `SHA256SUMS` (the exact tarballs packaged) and
  `build-rpms.sh`;
- **the RPMs** in rpm-repo, each stored as its own `rpm-<NVRA>` tag on GHCR
  (pushing a tag is not a git push, so the file limit does not apply);
- **the source RPMs**, which contain the original tarballs byte for byte.
  Keep them with the RPMs (see below).

## Building and registering

```bash
# 1. Put the tarballs in SOURCES/ (gitignored). build-rpms.sh refuses to run
#    if they do not match SHA256SUMS.
./build-rpms.sh                       # -> rpms/*.el9.*.rpm and *.src.rpm

# 2. Register the binary RPMs with gemini-rtsw-repo (needs docker login ghcr.io).
../gemini-rtsw-repo/upload-rpm.sh --tag-only \
    rpms/giapi-glue-cc-0.16-1.el9.x86_64.rpm \
    rpms/gmp-server-0.2.6-0.1.SNAPSHOT.el9.noarch.rpm
```

`--tag-only` pushes just the two packages; the next `publish` job of any
gemini-rtsw-ci repo (or `sync_repo.sh`) merges them into `rpm-repo:latest`.
Check with `../gemini-rtsw-repo/list_rpms.sh giapi gmp-server`.

To get the original tarball back from a source RPM:
`rpm2cpio giapi-glue-cc-0.16-1.el9.src.rpm | cpio -idv '*.tar.gz'`.

## Replacing a tarball

1. Put the new tarball in `SOURCES/`, update its line in `SHA256SUMS`, and bump
   `Version` or `Release` in its spec (with a `%changelog` entry saying where it
   came from).
2. `./build-rpms.sh`, then register as above.
3. Commit, and move `gnirsdc-data-manager`'s `BuildRequires` pin to the new
   NVR.

When the GIAPI glue is eventually built from source, that build becomes the
next `giapi-glue-cc` release, and nothing else changes.
