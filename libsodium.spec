#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# don't perform "make check"

Summary:	Portable NaCl-based crypto library
Summary(pl.UTF-8):	Przenośna biblioteka kryptograficzna oparta na NaCl
Name:		libsodium
Version:	1.0.19
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://download.libsodium.org/libsodium/releases/%{name}-%{version}.tar.gz
# Source0-md5:	0d8e2233fc41be6d4c7ee36d5dfe9416
URL:		https://libsodium.org/
BuildRequires:	pkgconfig >= 1:0.25
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NaCl (<http://nacl.cr.yp.to/>, pronounced "salt") is a new
easy-to-use high-speed software library for network communication,
encryption, decryption, signatures, etc.

NaCl's goal is to provide all of the core operations needed to build
higher-level cryptographic tools.

Sodium is a portable, cross-compilable, installable, packageable fork
of NaCl, with a compatible API.

%description -l pl.UTF-8
NaCl (<http://nacl.cr.yp.to/>, wymawiane jako "sól") to nowa szybka,
łatwa w użyciu biblioteka do komunikacji sieciowej, szyfrowania,
odszyfrowywania, podpisów itp.

Celem NaCl jest zapewnienie wszystkich głównych operacji niezbędnych
do tworzenia narzędzi kryptograficznych wyższego poziomu.

Sodium to przenośne, instalowalne i pakietowalne odgałęzienie NaCl ze
zgodnym API.

%package devel
Summary:	Header files for libsodium library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsodium
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libsodium library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libsodium.

%package static
Summary:	Static libsodium library
Summary(pl.UTF-8):	Statyczna biblioteka libsodium
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libsodium library.

%description static -l pl.UTF-8
Statyczna biblioteka libsodium.

%prep
%setup -q -n %{name}-stable

%build
%configure \
	--disable-silent-rules \
	%{__enable_disable static_libs static}

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsodium.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README.markdown THANKS
%attr(755,root,root) %{_libdir}/libsodium.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsodium.so.26

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsodium.so
%{_includedir}/sodium.h
%{_includedir}/sodium
%{_pkgconfigdir}/libsodium.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsodium.a
%endif
