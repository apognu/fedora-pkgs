%global debug_package %{nil}
%global __brp_strip %{nil}
%global __provides_exclude_from ^/opt/zen/.*$
%global __requires_exclude_from ^/opt/zen/.*$

Name:           zen-browser
Version:        1.24.2b
Release:        1%{?dist}
Summary:        Zen Browser, a Firefox-based browser focused on simplicity and design
License:        MPL-2.0
URL:            https://github.com/zen-browser/desktop
Source0:        %{url}/releases/download/%{version}/zen.linux-x86_64.tar.xz#/zen-%{version}.linux-x86_64.tar.xz
Source1:        zen-browser.desktop
Source2:        policies.json
Source3:        zen-browser
ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  patchelf

Requires:       hicolor-icon-theme

%description
Zen Browser is a fork of Firefox that aims to improve the browsing experience
by focusing on a simple, performant, private and beautifully designed browser.

This package repackages the official upstream binary release.

%prep
%setup -q -n zen

%install
install -d %{buildroot}/opt/zen
cp -a . %{buildroot}/opt/zen/

patchelf --set-rpath '$ORIGIN' %{buildroot}/opt/zen/libonnxruntime.so

install -Dm0644 %{SOURCE2} %{buildroot}/opt/zen/distribution/policies.json
install -Dm0755 %{SOURCE3} %{buildroot}%{_bindir}/zen-browser

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

for size in 16 32 48 64 128; do
  install -d %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
  ln -s /opt/zen/browser/chrome/icons/default/default${size}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/zen-browser.png
done

%files
/opt/zen/
%{_bindir}/zen-browser
%{_datadir}/applications/zen-browser.desktop
%{_datadir}/icons/hicolor/*/apps/zen-browser.png

%changelog
%autochangelog
