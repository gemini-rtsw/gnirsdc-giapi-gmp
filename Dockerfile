# Unpacked copies of the tarballs listed in RELEASES, for other images to COPY
# from. Nothing runs in it: it is a carrier, so it starts from scratch and holds
# nothing but the unpacked trees.
#
#   COPY --from=ghcr.io/gemini-rtsw/gnirsdc-giapi-gmp:<VERSION> /giapi-glue-cc /gnirsdc/giapi-glue-cc
#
# Run ./fetch-assets.sh first: it downloads and checksums the tarballs into
# assets/. ADD unpacks a local tar archive, so each one lands at / under the
# directory it was packed with.
FROM scratch
ADD assets/*.tar.gz /
