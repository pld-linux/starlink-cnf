Summary:	CNF - C aNd Fortran mixed programming
Summary(pl.UTF-8):	CNF - mieszanie kodu w C i Fortranie
Name:		starlink-cnf
Version:	4.0_2.218
Release:	2
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.starlink.rl.ac.uk/pub/ussc/store/cnf/cnf.tar.Z
# Source0-md5:	193897823c84e043a85b0f0c24b51e82
URL:		http://www.starlink.rl.ac.uk/static_www/soft_further_CNF.html
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	sed >= 4.0
BuildRequires:	starlink-htx
Requires:	starlink-htx
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		stardir		/usr/lib/star

%description
The CNF package comprises two sets of software which ease the task of
writing portable programs in a mixture of FORTRAN and C. F77 is a set
of C macros for handling the FORTRAN/C subroutine linkage in a
portable way, and CNF is a set of functions to handle the difference
between FORTRAN and C character strings, logical values and pointers
to dynamically allocated memory.

%description -l pl.UTF-8
Pakiet CNF łączy dwa zbiory oprogramowania ułatwiającego zadanie
pisania przenośnych programów z mieszanym kodem w Fortranie i C. F77
to zbiór makr C do obsługi linkowania funkcji Fortran/C w sposób
przenośny, a CNF to zbiór funkcji do obsługi różnic między Fortranem i
C w traktowaniu łańcuchów znaków, wartości logicznych i wskaźników do
dynamicznie przydzielanej pamięci.

%package devel
Summary:	Header files for CNF library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CNF
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for CNF library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CNF.

%package static
Summary:	Static Starlink CNF library
Summary(pl.UTF-8):	Statyczna biblioteka Starlink CNF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Starlink CNF library.

%description static -l pl.UTF-8
Statyczna biblioteka Starlink CNF.

%prep
%setup -q -c

sed -i -e "s@ -O'@ %{rpmcflags} -fPIC'@;s@ ld -shared -soname @ %{__cc} -shared -Wl,-soname=@" mk

%build
%ifarch %{x8664} alpha ia64 ppc64 s390x sparc64
# get version with 64-bit pointer type before mk unpacks 32-bit one
tar xf cnf_source.tar cnf_par_alpha_OSF1
mv -f cnf_par_alpha_OSF1 cnf_par
%endif

SYSTEM=ix86_Linux \
./mk build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{stardir}/help

SYSTEM=ix86_Linux \
./mk install \
	STARLINK=%{stardir} \
	INSTALL=$RPM_BUILD_ROOT%{stardir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc cnf.news
%{stardir}/dates/*
%docdir %{stardir}/docs
%{stardir}/docs/sun*
%attr(755,root,root) %{stardir}/share/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{stardir}/bin/cnf_dev
%attr(755,root,root) %{stardir}/bin/cnf_link*
%{stardir}/include/*

%files static
%defattr(644,root,root,755)
%{stardir}/lib/*.a
