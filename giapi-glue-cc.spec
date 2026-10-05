# giapi-glue-cc: the GIAPI C++ glue library, the instrument side of the Gemini
# Master Process interface, built by another Gemini team.
#
# NOT BUILT FROM SOURCE HERE. Source0 is the prebuilt Rocky 8 build tree
# (giapi-gluecc_rocky8.tar.gz: source, install/ with libgiapi-glue-cc, and
# external/ with activemq-cpp, log4cxx, apr, curl/curlpp, boost and their
# built libraries), packaged unchanged under /opt/giapi-glue-cc. It runs on EL9
# with libxcrypt-compat (libcrypt.so.1). Built locally with build-rpms.sh and
# registered with gemini-rtsw-repo/upload-rpm.sh -- see README.

# A prebuilt bundle: leave every file as it is (no strip, no debuginfo, no
# shebang mangling), and keep its bundled libraries out of the system-wide
# Provides/Requires.
%global debug_package %{nil}
%global __os_install_post %{nil}
%global _build_id_links none

Name:           giapi-glue-cc
Version:        0.16
Release:        1%{?dist}
Summary:        GIAPI C++ glue library (prebuilt Rocky 8 build tree)
License:        Proprietary
Source0:        giapi-gluecc_rocky8.tar.gz
ExclusiveArch:  x86_64
AutoReqProv:    no

BuildRequires:  libxcrypt-compat
Requires:       libxcrypt-compat

%description
GIAPI C++ glue library %{version} with its bundled external libraries, as the
prebuilt Rocky 8 build tree, installed at /opt/giapi-glue-cc. Set GIAPI_ROOT to
that directory, or source /opt/giapi-glue-cc/defineGiapiglueEnv.sh from it, to
get the library paths.

%prep
%setup -q -n giapi-glue-cc

%install
mkdir -p %{buildroot}/opt/giapi-glue-cc
cp -a . %{buildroot}/opt/giapi-glue-cc/

%check
# Every bundled shared library must resolve on this EL, against the bundle's
# own lib directories plus the system.
G=%{buildroot}/opt/giapi-glue-cc
export LD_LIBRARY_PATH=$G/external/apr/lib:$G/external/apr-util/lib:$G/external/activemq-cpp/lib:$G/external/log4cxx/lib:$G/external/curlpp/lib:$G/external/curlpp/lib64:$G/external/libcurl/lib:$G/external/libcurl/lib64:$G/install/lib
missing=$(find $G/install/lib $G/external/*/lib* -name '*.so*' -type f -exec ldd {} \; 2>/dev/null | grep 'not found' | sort -u)
[ -z "$missing" ] || { echo "ERROR: unresolved libraries:"; echo "$missing"; exit 1; }
test -f $G/install/lib/libgiapi-glue-cc.so.0.16

%files
/opt/giapi-glue-cc

%changelog
* Mon Oct 05 2026 Hawi Stecher <hawi.stecher@noirlab.edu> - 0.16-1
- Package the 2024-04 Rocky 8 build tree (giapi-gluecc_rocky8.tar.gz,
  sha256 a381e9ce...) for EL9; first committed to gnirsdc-data-manager in
  246b607.
