%global debug_package %{nil}

Name:           slk
Version:        0.52.0
Release:        1%{?dist}
Summary:        Keyboard-driven Slack TUI
License:        MIT
URL:            https://github.com/gammons/slk
Source0:        %{url}/releases/download/v%{version}/slk_%{version}_linux_x86_64.tar.gz
ExclusiveArch:  x86_64

%description
slk is a fast, keyboard-driven terminal client for Slack, with multiple
workspaces, threads, inline images and themes.

This package repackages the official upstream binary release.

%prep
%setup -q -c

%install
install -Dm0755 slk %{buildroot}%{_bindir}/slk

%check
./slk --version | grep -F '%{version}'

%files
%license LICENSE
%doc README.md
%{_bindir}/slk

%changelog
%autochangelog
