%global srcname vala-panel-appmenu
%global _vpath_srcdir subprojects/appmenu-glib-translator

Name:           appmenu-glib-translator
Version:        25.04
Release:        1%{?dist}
Summary:        Translator from DBusMenu to GMenuModel
License:        LGPL-3.0-or-later
URL:            https://gitlab.com/vala-panel-project/vala-panel-appmenu
Source0:        %{url}/-/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  vala
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)

%description
Library translating com.canonical.dbusmenu menus into GMenuModel, from the
vala-panel-appmenu project. Used by astal-tray.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, GIR, VAPI and pkg-config files for %{name}.

%prep
%autosetup -p1 -n %{srcname}-%{version}

# The subproject version is not bumped upstream, align it with the release
sed -i "s/^version : '[^']*'/version : '%{version}'/" %{_vpath_srcdir}/meson.build

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%{_libdir}/libappmenu-glib-translator.so.*
%{_libdir}/girepository-1.0/AppmenuGLibTranslator-%{version}.typelib

%files devel
%{_includedir}/appmenu-glib-translator/
%{_libdir}/libappmenu-glib-translator.so
%{_libdir}/pkgconfig/appmenu-glib-translator.pc
%{_datadir}/gir-1.0/AppmenuGLibTranslator-%{version}.gir
%{_datadir}/vala/vapi/appmenu-glib-translator.{deps,vapi}

%changelog
%autochangelog
