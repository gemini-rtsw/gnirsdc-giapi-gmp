# gmp-server: the Gemini Master Process server distribution (Java/OSGi, from
# the ASPEN repository), built by another Gemini team.
#
# NOT BUILT FROM SOURCE HERE. Source0 is the distribution tarball, packaged
# unchanged under /opt/gmp-server. Instruments supply their own conf/. Built
# locally with build-rpms.sh and registered with
# gemini-rtsw-repo/upload-rpm.sh -- see README.

%global debug_package %{nil}
%global __os_install_post %{nil}

Name:           gmp-server
Version:        0.2.6
# The distribution is 0.2.6-SNAPSHOT; SNAPSHOT sorts below a future 0.2.6-1.
Release:        0.1.SNAPSHOT%{?dist}
Summary:        Gemini Master Process server (prebuilt distribution)
License:        Proprietary
Source0:        gmp-server-%{version}-SNAPSHOT.tar.gz
BuildArch:      noarch
AutoReqProv:    no

# bin/gmp-server-ctl.sh runs java 8 from JAVA_HOME and uses ps.
Requires:       java-1.8.0-openjdk-headless
Requires:       procps-ng

%description
GMP server %{version}-SNAPSHOT (OSGi Felix, GDS keyword collection, GIAPI
services, ActiveMQ broker, web console), installed at /opt/gmp-server. Start
it with /opt/gmp-server/bin/gmp-server-ctl.sh after putting the instrument's
configuration in /opt/gmp-server/conf.

%prep
%setup -q -n gmp-server-%{version}-SNAPSHOT

%install
mkdir -p %{buildroot}/opt/gmp-server
cp -a . %{buildroot}/opt/gmp-server/

%check
test -x %{buildroot}/opt/gmp-server/bin/gmp-server-ctl.sh

%files
/opt/gmp-server

%changelog
* Mon Oct 05 2026 Hawi Stecher <hawi.stecher@noirlab.edu> - 0.2.6-0.1.SNAPSHOT
- Package the gmp-server-0.2.6-SNAPSHOT distribution (sha256 48b1283f...)
  for EL9; first committed to gnirsdc-data-manager in 14cee43.
