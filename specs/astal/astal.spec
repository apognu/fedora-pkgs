%global commit      b7aaf4ce69ebb3c5b1818d524e04b23bc755a97d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# Commit date as reported by nvchecker (YYYYMMDD.HHMMSS), keeps snapshots ordered
%global commitdate  20261108.102027

# Built in dependency order
%global astal_libs astal/io quarrel wl/wl astal/gtk3 astal/gtk4 wl/wl4 apps auth battery bluetooth brightness cava greet hyprland idle-notify mpris network notifd powerprofiles river tray wireplumber workspace

Name:           astal
Version:        0~git%{commitdate}.%{shortcommit}
Release:        1%{?dist}
Summary:        Building blocks for creating custom desktop shells
License:        LGPL-2.1-only
URL:            https://github.com/Aylur/astal
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf
BuildRequires:  python3
BuildRequires:  vala
BuildRequires:  valadoc
BuildRequires:  wl-vapi-gen
BuildRequires:  /usr/bin/g-ir-compiler
BuildRequires:  pkgconfig(appmenu-glib-translator)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-layer-shell-0)
BuildRequires:  pkgconfig(gtk4-wayland)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libcava)
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wireplumber-0.5)

Requires:       %{name}-io%{?_isa} = %{version}-%{release}
Requires:       %{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:       %{name}-gtk4%{?_isa} = %{version}-%{release}
Requires:       %{name}-quarrel%{?_isa} = %{version}-%{release}
Requires:       %{name}-wl%{?_isa} = %{version}-%{release}
Requires:       %{name}-wl4%{?_isa} = %{version}-%{release}
Requires:       %{name}-apps%{?_isa} = %{version}-%{release}
Requires:       %{name}-auth%{?_isa} = %{version}-%{release}
Requires:       %{name}-battery%{?_isa} = %{version}-%{release}
Requires:       %{name}-bluetooth%{?_isa} = %{version}-%{release}
Requires:       %{name}-brightness%{?_isa} = %{version}-%{release}
Requires:       %{name}-cava%{?_isa} = %{version}-%{release}
Requires:       %{name}-greet%{?_isa} = %{version}-%{release}
Requires:       %{name}-hyprland%{?_isa} = %{version}-%{release}
Requires:       %{name}-idle-notify%{?_isa} = %{version}-%{release}
Requires:       %{name}-mpris%{?_isa} = %{version}-%{release}
Requires:       %{name}-network%{?_isa} = %{version}-%{release}
Requires:       %{name}-notifd%{?_isa} = %{version}-%{release}
Requires:       %{name}-powerprofiles%{?_isa} = %{version}-%{release}
Requires:       %{name}-river%{?_isa} = %{version}-%{release}
Requires:       %{name}-tray%{?_isa} = %{version}-%{release}
Requires:       %{name}-wireplumber%{?_isa} = %{version}-%{release}
Requires:       %{name}-workspace%{?_isa} = %{version}-%{release}

%description
Astal is a collection of GObject libraries for building desktop shells.

This metapackage installs all Astal libraries.

%package io
Summary:        Astal core IPC and utility library

%description io
Core IPC and utility library, part of the Astal desktop shell libraries.

%package gtk3
Summary:        Astal GTK 3 widgets and application library
# The typelib references cairo-1.0, shipped by gobject-introspection
Requires:       gobject-introspection

%description gtk3
GTK 3 widgets and application library, part of the Astal desktop shell libraries.

%package gtk4
Summary:        Astal GTK 4 widgets and application library
# The typelib references cairo-1.0, shipped by gobject-introspection
Requires:       gobject-introspection

%description gtk4
GTK 4 widgets and application library, part of the Astal desktop shell libraries.

%package quarrel
Summary:        Astal command line argument parsing library

%description quarrel
Command line argument parsing library, part of the Astal desktop shell libraries.

%package wl
Summary:        Astal Wayland client helper library

%description wl
Wayland client helper library, part of the Astal desktop shell libraries.

%package wl4
Summary:        Astal Wayland helper library for GTK 4

%description wl4
Wayland helper library for GTK 4, part of the Astal desktop shell libraries.

%package apps
Summary:        Astal application launcher library

%description apps
Application launcher library, part of the Astal desktop shell libraries.

%package auth
Summary:        Astal PAM authentication library

%description auth
PAM authentication library, part of the Astal desktop shell libraries.

%package battery
Summary:        Astal UPower battery library
Recommends:     upower

%description battery
UPower battery library, part of the Astal desktop shell libraries.

%package bluetooth
Summary:        Astal BlueZ bluetooth library
Recommends:     bluez

%description bluetooth
BlueZ bluetooth library, part of the Astal desktop shell libraries.

%package brightness
Summary:        Astal Display and keyboard brightness library

%description brightness
Display and keyboard brightness library, part of the Astal desktop shell libraries.

%package cava
Summary:        Astal Audio visualizer library

%description cava
Audio visualizer library, part of the Astal desktop shell libraries.

%package greet
Summary:        Astal greetd client library

%description greet
greetd client library, part of the Astal desktop shell libraries.

%package hyprland
Summary:        Astal Hyprland IPC library

%description hyprland
Hyprland IPC library, part of the Astal desktop shell libraries.

%package idle-notify
Summary:        Astal Wayland idle notification library

%description idle-notify
Wayland idle notification library, part of the Astal desktop shell libraries.

%package mpris
Summary:        Astal MPRIS media player library

%description mpris
MPRIS media player library, part of the Astal desktop shell libraries.

%package network
Summary:        Astal NetworkManager library
Recommends:     NetworkManager

%description network
NetworkManager library, part of the Astal desktop shell libraries.

%package notifd
Summary:        Astal Notification daemon library

%description notifd
Notification daemon library, part of the Astal desktop shell libraries.

%package powerprofiles
Summary:        Astal power-profiles-daemon library
Recommends:     power-profiles-daemon

%description powerprofiles
power-profiles-daemon library, part of the Astal desktop shell libraries.

%package river
Summary:        Astal River compositor IPC library

%description river
River compositor IPC library, part of the Astal desktop shell libraries.

%package tray
Summary:        Astal StatusNotifierItem system tray library

%description tray
StatusNotifierItem system tray library, part of the Astal desktop shell libraries.

%package wireplumber
Summary:        Astal WirePlumber audio library
Recommends:     wireplumber

%description wireplumber
WirePlumber audio library, part of the Astal desktop shell libraries.

%package workspace
Summary:        Astal Wayland workspace management library

%description workspace
Wayland workspace management library, part of the Astal desktop shell libraries.

%package devel
Summary:        Development files for Astal
Requires:       %{name}-io%{?_isa} = %{version}-%{release}
Requires:       %{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:       %{name}-gtk4%{?_isa} = %{version}-%{release}
Requires:       %{name}-quarrel%{?_isa} = %{version}-%{release}
Requires:       %{name}-wl%{?_isa} = %{version}-%{release}
Requires:       %{name}-wl4%{?_isa} = %{version}-%{release}
Requires:       %{name}-apps%{?_isa} = %{version}-%{release}
Requires:       %{name}-auth%{?_isa} = %{version}-%{release}
Requires:       %{name}-battery%{?_isa} = %{version}-%{release}
Requires:       %{name}-bluetooth%{?_isa} = %{version}-%{release}
Requires:       %{name}-brightness%{?_isa} = %{version}-%{release}
Requires:       %{name}-cava%{?_isa} = %{version}-%{release}
Requires:       %{name}-greet%{?_isa} = %{version}-%{release}
Requires:       %{name}-hyprland%{?_isa} = %{version}-%{release}
Requires:       %{name}-idle-notify%{?_isa} = %{version}-%{release}
Requires:       %{name}-mpris%{?_isa} = %{version}-%{release}
Requires:       %{name}-network%{?_isa} = %{version}-%{release}
Requires:       %{name}-notifd%{?_isa} = %{version}-%{release}
Requires:       %{name}-powerprofiles%{?_isa} = %{version}-%{release}
Requires:       %{name}-river%{?_isa} = %{version}-%{release}
Requires:       %{name}-tray%{?_isa} = %{version}-%{release}
Requires:       %{name}-wireplumber%{?_isa} = %{version}-%{release}
Requires:       %{name}-workspace%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config files, GObject introspection data and Vala bindings for
the Astal libraries.

%prep
%autosetup -p1 -n %{name}-%{commit}

%build
# Libraries depend on each other, so they are built and installed
# one after another in %%install.

%install
%set_build_flags

# Relocate .pc files found in the buildroot, so libraries can be built against
# the ones installed just before. A wrapper is needed since g-ir-scanner treats
# $PKG_CONFIG as a single executable.
cat > %{_builddir}/astal-pkgconf << 'EOF'
#!/bin/sh
exec pkgconf --define-prefix "$@"
EOF
chmod +x %{_builddir}/astal-pkgconf

export PKG_CONFIG=%{_builddir}/astal-pkgconf
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig:%{buildroot}%{_datadir}/pkgconfig
export XDG_DATA_DIRS=%{buildroot}%{_datadir}:%{_datadir}
export GI_TYPELIB_PATH=%{buildroot}%{_libdir}/girepository-1.0
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}

# Some headers (e.g. astal-io.h) are installed to the top-level includedir,
# which pkg-config omits from Cflags since it's a system directory. Debug info
# must not reference the buildroot, hence the prefix map.
export CFLAGS="$CFLAGS -I%{buildroot}%{_includedir} -ffile-prefix-map=%{buildroot}="
export LDFLAGS="$LDFLAGS -L%{buildroot}%{_libdir}"

for lib in %{astal_libs}; do
  srcdir="lib/$lib"
  builddir="build/$lib"

  %{shrink:%{__meson} setup
    --buildtype=plain
    --prefix=%{_prefix}
    --libdir=%{_libdir}
    --libexecdir=%{_libexecdir}
    --bindir=%{_bindir}
    --sbindir=%{_sbindir}
    --includedir=%{_includedir}
    --datadir=%{_datadir}
    --mandir=%{_mandir}
    --infodir=%{_infodir}
    --localedir=%{_datadir}/locale
    --sysconfdir=%{_sysconfdir}
    --localstatedir=%{_localstatedir}
    --sharedstatedir=%{_sharedstatedir}
    --wrap-mode=nodownload
    --auto-features=enabled
    "$srcdir" "$builddir"}

  %{__meson} compile -C "$builddir" --verbose
  DESTDIR=%{buildroot} %{__meson} install -C "$builddir" --no-rebuild
done

%files
%license LICENSE

%files io
%license LICENSE
%{_bindir}/astal
%{_libdir}/libastal-io.so.0*
%{_libdir}/girepository-1.0/AstalIO-0.1.typelib

%files gtk3
%license LICENSE
%{_libdir}/libastal.so.3*
%{_libdir}/girepository-1.0/Astal-3.0.typelib

%files gtk4
%license LICENSE
%{_libdir}/libastal-4.so.4*
%{_libdir}/girepository-1.0/Astal-4.0.typelib

%files quarrel
%license LICENSE
%{_libdir}/libquarrel.so.0*
%{_libdir}/girepository-1.0/Quarrel-0.1.typelib

%files wl
%license LICENSE
%{_libdir}/libastal-wl.so.0*
%{_libdir}/girepository-1.0/AstalWl-0.1.typelib

%files wl4
%license LICENSE
%{_libdir}/libastal-wl4.so.0*
%{_libdir}/girepository-1.0/AstalWl4-0.1.typelib

%files apps
%license LICENSE
%{_bindir}/astal-apps
%{_libdir}/libastal-apps.so.0*
%{_libdir}/girepository-1.0/AstalApps-0.1.typelib

%files auth
%license LICENSE
%{_bindir}/astal-auth
%{_libdir}/libastal-auth.so.0*
%{_libdir}/girepository-1.0/AstalAuth-0.1.typelib
%config(noreplace) %{_sysconfdir}/pam.d/astal-auth

%files battery
%license LICENSE
%{_bindir}/astal-battery
%{_libdir}/libastal-battery.so.0*
%{_libdir}/girepository-1.0/AstalBattery-0.1.typelib

%files bluetooth
%license LICENSE
%{_libdir}/libastal-bluetooth.so.0*
%{_libdir}/girepository-1.0/AstalBluetooth-0.1.typelib

%files brightness
%license LICENSE
%{_bindir}/astal-brightness
%{_libdir}/libastal-brightness.so.0*
%{_libdir}/girepository-1.0/AstalBrightness-0.1.typelib

%files cava
%license LICENSE
%{_libdir}/libastal-cava.so.0*
%{_libdir}/girepository-1.0/AstalCava-0.1.typelib

%files greet
%license LICENSE
%{_bindir}/astal-greet
%{_libdir}/libastal-greet.so.0*
%{_libdir}/girepository-1.0/AstalGreet-0.1.typelib

%files hyprland
%license LICENSE
%{_bindir}/astal-hyprland
%{_libdir}/libastal-hyprland.so.0*
%{_libdir}/girepository-1.0/AstalHyprland-0.1.typelib

%files idle-notify
%license LICENSE
%{_libdir}/libastal-idle-notify.so.0*
%{_libdir}/girepository-1.0/AstalIdleNotify-0.1.typelib

%files mpris
%license LICENSE
%{_bindir}/astal-mpris
%{_libdir}/libastal-mpris.so.0*
%{_libdir}/girepository-1.0/AstalMpris-0.1.typelib

%files network
%license LICENSE
%{_libdir}/libastal-network.so.0*
%{_libdir}/girepository-1.0/AstalNetwork-0.1.typelib

%files notifd
%license LICENSE
%{_bindir}/astal-notifd
%{_libdir}/libastal-notifd.so.0*
%{_libdir}/girepository-1.0/AstalNotifd-0.1.typelib
%{_datadir}/glib-2.0/schemas/io.astal.notifd.gschema.xml

%files powerprofiles
%license LICENSE
%{_bindir}/astal-power-profiles
%{_libdir}/libastal-power-profiles.so.0*
%{_libdir}/girepository-1.0/AstalPowerProfiles-0.1.typelib

%files river
%license LICENSE
%{_libdir}/libastal-river.so.0*
%{_libdir}/girepository-1.0/AstalRiver-0.1.typelib

%files tray
%license LICENSE
%{_bindir}/astal-tray
%{_libdir}/libastal-tray.so.0*
%{_libdir}/girepository-1.0/AstalTray-0.1.typelib

%files wireplumber
%license LICENSE
%{_libdir}/libastal-wireplumber.so.0*
%{_libdir}/girepository-1.0/AstalWp-0.1.typelib

%files workspace
%license LICENSE
%{_bindir}/astal-workspace
%{_libdir}/libastal-workspace.so.0*
%{_libdir}/girepository-1.0/AstalWorkspace-0.1.typelib

%files devel
%{_includedir}/astal.h
%{_includedir}/astal-*.h
%{_includedir}/astal/
%{_includedir}/quarrel.h
%{_libdir}/libastal*.so
%{_libdir}/libquarrel.so
%{_libdir}/pkgconfig/astal-*.pc
%{_libdir}/pkgconfig/quarrel-0.1.pc
%{_datadir}/gir-1.0/Astal*.gir
%{_datadir}/gir-1.0/Quarrel-0.1.gir
%{_datadir}/vala/vapi/astal-*.deps
%{_datadir}/vala/vapi/astal-*.vapi
%{_datadir}/vala/vapi/quarrel-0.1.vapi

%changelog
%autochangelog
