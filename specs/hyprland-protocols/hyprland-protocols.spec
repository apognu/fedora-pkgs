%global debug_package %{nil}

Name:           hyprland-protocols
Version:        0.8.0
Release:        1%{?dist}
Summary:        Wayland protocol extensions for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-protocols
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  ninja-build

%description
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Wayland protocol XML files for Hyprland.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%doc README.md
%license LICENSE

%files devel
%{_datadir}/%{name}/
%{_datadir}/pkgconfig/%{name}.pc

%changelog
%autochangelog
