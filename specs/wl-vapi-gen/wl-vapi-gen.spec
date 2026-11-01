Name:           wl-vapi-gen
Version:        1.1.0
Release:        1%{?dist}
Summary:        Generate Vala bindings from Wayland protocol XML files
License:        MIT
URL:            https://github.com/kotontrion/wl-vapi-gen
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  meson
BuildRequires:  python3-devel

Requires:       python3

%description
Tool generating Vala API files (VAPI) from Wayland protocol descriptions.

%package devel
Summary:        pkg-config file for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
pkg-config file allowing build systems to locate %{name}.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

chmod 0755 %{buildroot}%{_bindir}/wl-vapi-gen
%py3_shebang_fix %{buildroot}%{_bindir}/wl-vapi-gen

%files
%license LICENSE
%doc README.md
%{_bindir}/wl-vapi-gen

%files devel
%{_datadir}/pkgconfig/wl-vapi-gen.pc

%changelog
%autochangelog
