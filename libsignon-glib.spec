#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# testsuite build [switch broken in configure]

Summary:	Single signon authentication library for GLib applications
Summary(pl.UTF-8):	Biblioteka pojedynczego uwierzytelniania dla aplikacji opartych na bibliotece GLib
Name:		libsignon-glib
Version:	1.14
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://gitlab.com/accounts-sso/libsignon-glib/tags?sort=updated_desc
Source0:	https://gitlab.com/accounts-sso/libsignon-glib/repository/archive.tar.bz2?ref=VERSION_%{version}&fake_out=/%{name}-%{version}.tar.bz2
# Source0-md5:	494936de3c57cd12c3115707be2ca20e
URL:		https://gitlab.com/accounts-sso/libsignon-glib
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
%{?with_tests:BuildRequires:	check-devel >= 0.9.4}
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	python-pygobject3-devel >= 3.0
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	signon-devel >= 8.40
Requires:	glib2 >= 1:2.36
Requires:	signon-libs >= 8.40
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project is a library for managing single signon credentials which
can be used from GLib applications. It is effectively a GLib binding
for the D-Bus API provided by signond. It is part of the accounts-sso
project.

%description -l pl.UTF-8
Ten projekt to biblioteka do zarządzania danymi uwierzytelniającymi do
pojedynczego logowania, z której można korzystać w aplikacjach
opartych na bibliotece GLib. Jest to część projektu accounts-sso.

%package devel
Summary:	Development files for libsignon-glib library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libsignon-glib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36
Requires:	signon-devel >= 8.40

%description devel
Development files for libsignon-glib library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki libsignon-glib.

%package static
Summary:	Static libsignon-glib library
Summary(pl.UTF-8):	Statyczna biblioteka libsignon-glib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libsignon-glib library.

%description static -l pl.UTF-8
Statyczna biblioteka libsignon-glib.

%package apidocs
Summary:	API documentation for libsignon-glib library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libsignon-glib
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libsignon-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libsignon-glib.

%package -n python-libsignon-glib
Summary:	Python bindings for libsignon-glib
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libsignon-glib
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygobject3 >= 3

%description -n python-libsignon-glib
Python bindings for libsignon-glib.

%description -n python-libsignon-glib -l pl.UTF-8
Wiązania Pythona do biblioteki libsignon-glib.

%package -n vala-libsignon-glib
Summary:	Vala API for libsignon-glib
Summary(pl.UTF-8):	API języka Vala do biblioteki libsignon-glib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-libsignon-glib
Vala API for libsignon-glib.

%description -n vala-libsignon-glib -l pl.UTF-8
API języka Vala do biblioteki libsignon-glib.

%prep
%setup -q -n %{name}-VERSION_%{version}-e90302e342bfd27bc8c9132ab9d0ea3d8723fd03

%build
%{__gtkdocize} --flavour no-tmpl
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{!?with_tests:--disable-tests} \
	--with-html-dir=%{_gtkdocdir}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm}	$RPM_BUILD_ROOT%{_libdir}/libsignon-glib.la

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_libdir}/libsignon-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsignon-glib.so.1
%{_libdir}/girepository-1.0/Signon-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsignon-glib.so
%{_datadir}/gir-1.0/Signon-1.0.gir
%{_includedir}/libsignon-glib
%{_pkgconfigdir}/libsignon-glib.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsignon-glib.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libsignon-glib

%files -n python-libsignon-glib
%defattr(644,root,root,755)
%{py_sitedir}/gi/overrides/Signon.py[co]

%files -n vala-libsignon-glib
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/signon.vapi
