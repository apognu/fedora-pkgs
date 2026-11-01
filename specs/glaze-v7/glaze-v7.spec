# Header-only glaze 7.x, installed in a versioned location so it does not
# conflict with Fedora's glaze package. Used by Hyprland.

%global debug_package %{nil}

Name:           glaze-v7
Version:        7.9.1
Release:        1%{?dist}
Summary:        Extremely fast, in memory, JSON and interface library (v7)
License:        MIT
URL:            https://github.com/stephenberry/glaze
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build

%description
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Header-only glaze %{version}, installed under %{_includedir}/glaze-v7.

%prep
%autosetup -p1 -n glaze-%{version}

%build
%cmake \
  -DBUILD_TESTING=OFF \
  -Dglaze_DEVELOPER_MODE=OFF \
  -Dglaze_BUILD_EXAMPLES=OFF \
  -DCMAKE_INSTALL_INCLUDEDIR=include/glaze-v7 \
  -Dglaze_INSTALL_CMAKEDIR=%{_datadir}/glaze-v7
%cmake_build

%install
%cmake_install

%files
%doc README.md
%license LICENSE

%files devel
%{_datadir}/glaze-v7/
%{_includedir}/glaze-v7/

%changelog
%autochangelog
