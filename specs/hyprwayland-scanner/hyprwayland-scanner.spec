Name:           hyprwayland-scanner
Version:        0.4.6
Release:        1%{?dist}
Summary:        A Hyprland implementation of wayland-scanner, in and for C++
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwayland-scanner
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(pugixml)

%description
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_bindir}/hyprwayland-scanner

%files devel
%{_libdir}/cmake/hyprwayland-scanner/
%{_libdir}/pkgconfig/hyprwayland-scanner.pc

%changelog
%autochangelog
