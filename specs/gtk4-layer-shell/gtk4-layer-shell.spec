Name:           gtk4-layer-shell
Version:        1.3.0
# Supersede the 1.3.0-10 build previously provided by nett00n/hyprland.
Release:        11%{?dist}
Summary:        Library to create desktop components for Wayland using GTK 4
License:        MIT
URL:            https://github.com/wmww/gtk4-layer-shell
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  vala
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)

%description
Library for building panels, notifications, wallpapers and other desktop
components with GTK 4 using the Wayland layer shell protocol.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, GIR, VAPI and pkg-config files for %{name}.

%prep
%autosetup -p1

%build
%meson -Dexamples=false -Ddocs=false -Dtests=false -Dintrospection=true -Dvapi=true
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libgtk4-layer-shell.so.*
%{_libdir}/liblayer-shell-preload.so
%{_libdir}/girepository-1.0/Gtk4LayerShell-1.0.typelib
%{_libdir}/girepository-1.0/Gtk4SessionLock-1.0.typelib

%files devel
%{_includedir}/gtk4-layer-shell/
%{_libdir}/libgtk4-layer-shell.so
%{_libdir}/pkgconfig/gtk4-layer-shell-0.pc
%{_datadir}/gir-1.0/Gtk4LayerShell-1.0.gir
%{_datadir}/gir-1.0/Gtk4SessionLock-1.0.gir
%{_datadir}/vala/vapi/gtk4-layer-shell-0.{deps,vapi}

%changelog
%autochangelog
