Name:           hyprland
Version:        0.57.1
Release:        1%{?dist}
Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  aquamarine-devel
BuildRequires:  glaze-v7-devel
BuildRequires:  glslang-devel
BuildRequires:  hyprcursor-devel
BuildRequires:  hyprgraphics-devel
BuildRequires:  hyprland-protocols-devel
BuildRequires:  hyprlang-devel
BuildRequires:  hyprutils-devel
BuildRequires:  hyprwayland-scanner-devel
BuildRequires:  hyprwire-devel
%if 0%{?fedora} >= 45
BuildRequires:  pkgconfig(lua) >= 5.5
%else
BuildRequires:  lua5.5-devel
%endif
BuildRequires:  readline-devel
BuildRequires:  udis86-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libeis-1.0)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(muparser)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  systemd-rpm-macros

Requires:       hyprland-guiutils
Requires:       xorg-x11-server-Xwayland
Recommends:     uwsm
Recommends:     xdg-desktop-portal-hyprland

%description
Hyprland is a dynamic tiling Wayland compositor that doesn't sacrifice on its
looks.

%package devel
Summary:        Header and protocol files for Hyprland plugins
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       aquamarine-devel
Requires:       hyprcursor-devel
Requires:       hyprgraphics-devel
Requires:       hyprlang-devel
Requires:       hyprutils-devel

%description devel
Header and protocol files needed to build Hyprland plugins.

%prep
%autosetup -p1 -n Hyprland-%{version}

%build
%cmake \
  -DNO_TESTS=ON \
  -DBUILD_TESTING=OFF \
  -Dglaze_DIR=%{_datadir}/glaze-v7
%cmake_build

%install
%cmake_install

# Upstream installs the target in $libdir/systemd/user.
mkdir -p %{buildroot}%{_userunitdir}
mv %{buildroot}%{_libdir}/systemd/user/hyprland-session.target %{buildroot}%{_userunitdir}/
rm -rf %{buildroot}%{_libdir}/systemd

%files
%license LICENSE
%doc README.md
%{_bindir}/Hyprland
%{_bindir}/hyprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_bindir}/start-hyprland
%{_datadir}/bash-completion/completions/*
%{_datadir}/fish/vendor_completions.d/*
%{_datadir}/zsh/site-functions/*
%{_datadir}/hypr/
%{_datadir}/wayland-sessions/hyprland*.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_mandir}/man1/hyprctl.1*
%{_mandir}/man1/Hyprland.1*
%{_userunitdir}/hyprland-session.target

%files devel
%{_includedir}/hyprland/
%{_datadir}/pkgconfig/hyprland.pc

%changelog
%autochangelog
