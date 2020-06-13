Name:           twuewand
Version:        3.0.0
Release:        1%{?dist}
Summary:        twuewand random number generator
License:        GPLv2+
URL:            https://www.finnie.org/software/twuewand
Source0:        https://www.finnie.org/software/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
twuewand is software that creates hardware-generated random data.  It
accomplishes this by exploiting the fact that the CPU clock and the
RTC (real-time clock) are physically separate, and that time and work
are not linked.

%prep
%autosetup

%build
%py3_build
make -C rndaddentropy

%install
%py3_install
make -C rndaddentropy install PREFIX=/usr DESTDIR=%{buildroot}
install -Dp -m 0644 doc/twuewand.1 %{buildroot}/%{_mandir}/man1
install -Dp -m 0644 doc/rndaddentropy.1 %{buildroot}/%{_mandir}/man1

%files
%doc README.md
%license COPYING
%{python3_sitelib}/*
%{_bindir}/%{name}
%{_bindir}/rndaddentropy
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/rndaddentropy.1*
