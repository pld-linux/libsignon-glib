#
# Conditional build:
%bcond_without	python2		# Python 2.x binding (deprecated, not supported upstream)
%bcond_without	static_libs	# static library
%bcond_without	tests		# testsuite build [switch broken in configure]

Summary:	Single signon authentication library for GLib applications
Summary(pl.UTF-8):	Biblioteka pojedynczego uwierzytelniania dla aplikacji opartych na bibliotece GLib
Name:		libsignon-glib
Version:	2.1
Release:	6
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://gitlab.com/accounts-sso/libsignon-glib/tags
Source0:	https://gitlab.com/accounts-sso/libsignon-glib/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	9558f1e6658b4fad34420349edd41439
# submodule
Source1:	https://gitlab.com/accounts-sso/signon-dbus-specification/-/archive/67487954653006ebd0743188342df65342dc8f9b/signon-dbus-specification-67487954653006ebd0743188342df65342dc8f9b.tar.bz2
# Source1-md5:	21f2a3bf51a6c7eb6f74a2d3c776fcb9
URL:		https://gitlab.com/accounts-sso/libsignon-glib
%{?with_tests:BuildRequires:	check-devel >= 0.9.4}
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-pygobject3-devel >= 3.0}
BuildRequires:	python3-pygobject3-devel >= 3.0
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	vala
Requires:	glib2 >= 1:2.36
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
BuildArch:	noarch

%description apidocs
API documentation for libsignon-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libsignon-glib.

%package -n python-libsignon-glib
Summary:	Python 2 bindings for libsignon-glib
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki libsignon-glib
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygobject3 >= 3

%description -n python-libsignon-glib
Python 2 bindings for libsignon-glib.

%description -n python-libsignon-glib -l pl.UTF-8
Wiązania Pythona 2 do biblioteki libsignon-glib.

%package -n python3-libsignon-glib
Summary:	Python 3 bindings for libsignon-glib
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libsignon-glib
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-pygobject3 >= 3

%description -n python3-libsignon-glib
Python 3 bindings for libsignon-glib.

%description -n python3-libsignon-glib -l pl.UTF-8
Wiązania Pythona 3 do biblioteki libsignon-glib.

%package -n vala-libsignon-glib
Summary:	Vala API for libsignon-glib
Summary(pl.UTF-8):	API języka Vala do biblioteki libsignon-glib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-libsignon-glib
Vala API for libsignon-glib.

%description -n vala-libsignon-glib -l pl.UTF-8
API języka Vala do biblioteki libsignon-glib.

%prep
%setup -q
tar xf %{SOURCE1} -C libsignon-glib/interfaces --strip-components 1

%if %{with static_libs}
%{__sed} -i -e '/^libsignon_glib_lib =/ s/shared_library/library/' libsignon-glib/meson.build
%endif

%build
%meson build \
	-Ddocumentation=true \
	-Dintrospection=true \
	-Dpython=true \
	-Dtests=%{__true_false tests}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}/gi/overrides
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}/gi/overrides

%if %{with python2}
install -d $RPM_BUILD_ROOT%{py_sitedir}/gi/overrides
cp -p pygobject/Signon.py $RPM_BUILD_ROOT%{py_sitedir}/gi/overrides
%py_comp $RPM_BUILD_ROOT%{py_sitedir}/gi/overrides
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/gi/overrides
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libsignon-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsignon-glib.so.2
%{_libdir}/girepository-1.0/Signon-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsignon-glib.so
%{_datadir}/gir-1.0/Signon-2.0.gir
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

%if %{with python2}
%files -n python-libsignon-glib
%defattr(644,root,root,755)
%{py_sitedir}/gi/overrides/Signon.py[co]
%endif

%files -n python3-libsignon-glib
%defattr(644,root,root,755)
%{py3_sitedir}/gi/overrides/Signon.py
%{py3_sitedir}/gi/overrides/__pycache__/Signon.cpython-*.py[co]

%files -n vala-libsignon-glib
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libsignon-glib.deps
%{_datadir}/vala/vapi/libsignon-glib.vapi
