Name:           twuewand
Version:        1.1+dev
Release:        1%{?dist}
Summary:        A bi-directional ping utility

Group:          Applications/System
License:        GPLv2+
URL:            http://www.finnie.org/software/twuewand/
Source0:        http://www.finnie.org/software/twuewand/twuewand-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
twuewand is software that creates hardware-generated random data.  It 
accomplishes this by exploiting the fact that the CPU clock and the 
RTC (real-time clock) are physically separate, and that time and work 
are not linked.


%prep
%setup -q


%build
make EXTRAVERSION=-$RPM_PACKAGE_RELEASE


%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=/usr DESTDIR=$RPM_BUILD_ROOT
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/man/man8
install -m 0755 twuewand.8 $RPM_BUILD_ROOT/usr/share/man/man8
install -m 0755 rndaddentropy.8 $RPM_BUILD_ROOT/usr/share/man/man8


%clean
make clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/usr/bin/twuewand
/usr/sbin/rndaddentropy
/usr/share/man/man8/twuewand.8.gz
/usr/share/man/man8/rndaddentropy.8.gz
%doc README
%doc COPYING


%changelog
