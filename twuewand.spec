Name: twuewand
Version: 3.0.0
Release: 1%{?dist}
Summary: twuewand random number generator

Group: Applications/System
License: GPLv2+
Url: http://www.finnie.org/software/twuewand/
Source0: http://www.finnie.org/software/twuewand/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Prefix: %{_prefix}
Vendor: Ryan Finnie <ryan@finnie.org>

%description
twuewand is software that creates hardware-generated random data.  It
accomplishes this by exploiting the fact that the CPU clock and the
RTC (real-time clock) are physically separate, and that time and work
are not linked.

%prep
%setup -q -n %{name}-%{version}

%build
python setup.py build
make -C rndaddentropy

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
make -C rndaddentropy install PREFIX=/usr DESTDIR=$RPM_BUILD_ROOT
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/man/man1
install -m 0755 doc/twuewand.1 $RPM_BUILD_ROOT/usr/share/man/man1
install -m 0755 doc/rndaddentropy.1 $RPM_BUILD_ROOT/usr/share/man/man1


%clean
python setup.py clean
make -C rndaddentropy clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
/usr/sbin/rndaddentropy
/usr/share/man/man1/twuewand.1.gz
/usr/share/man/man1/rndaddentropy.1.gz
%doc README
%doc COPYING
