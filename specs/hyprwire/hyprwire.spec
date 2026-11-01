Name:           hyprwire
Version:        0.3.1
Release:        1%{?dist}
Summary:        A fast and consistent wire protocol for IPC
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwire
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  hyprutils-devel
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(pugixml)

%description
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files and protocol scanner for %{name}.

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_libdir}/libhyprwire.so.*

%files devel
%{_bindir}/hyprwire-scanner
%{_includedir}/hyprwire/
%{_libdir}/libhyprwire.so
%{_libdir}/cmake/hyprwire-scanner/
%{_libdir}/pkgconfig/hyprwire-scanner.pc
%{_libdir}/pkgconfig/hyprwire.pc

%changelog
%autochangelog
