# LTO link fails (lto-wrapper error), like in the upstream Fedora cava package
%global _lto_cflags %{nil}

Name:           libcava
Version:        1.0.0
Release:        1%{?dist}
Summary:        Fork of cava providing it as a shared library
License:        MIT
URL:            https://github.com/LukashonakV/cava
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  alsa-lib-devel
BuildRequires:  iniparser-devel
BuildRequires:  portaudio-devel
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-simple)

%description
Console-based Audio Visualizer for ALSA, PulseAudio, PipeWire, JACK and
PortAudio, packaged as a shared library (used by astal-cava).

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config file for %{name}.

%prep
%autosetup -p1 -n cava-%{version}

%build
%meson \
  -Dbuild_target=lib \
  -Dcava_font=false \
  -Dinput_alsa=enabled \
  -Dinput_jack=enabled \
  -Dinput_pipewire=enabled \
  -Dinput_portaudio=enabled \
  -Dinput_pulse=enabled \
  -Dinput_oss=disabled \
  -Dinput_sndio=disabled \
  -Doutput_ncurses=disabled \
  -Doutput_sdl=disabled \
  -Doutput_sdl_glsl=disabled \
  -Dasan=disabled \
  -Dtsan=disabled \
  -Dubsan=disabled
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libcava.so.*

%files devel
%{_includedir}/cava/
%{_libdir}/libcava.so
%{_libdir}/pkgconfig/libcava.pc

%changelog
%autochangelog
