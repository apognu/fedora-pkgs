# Parallel-installable Lua 5.5 library, needed by Hyprland >= 0.57.
# Drop this package once Fedora ships Lua 5.5 in its main repositories.

%global major_version 5.5

Name:           lua5.5
Version:        5.5.1
Release:        1%{?dist}
Summary:        Lua %{major_version} shared library (parallel-installable)
License:        MIT
URL:            https://www.lua.org/
Source0:        https://www.lua.org/ftp/lua-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Lua is a powerful, light-weight programming language designed for extending
applications. This package provides the Lua %{major_version} shared library,
installed alongside the system Lua without conflicting with it.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config file for building against Lua %{major_version}.

%prep
%autosetup -n lua-%{version}

sed -i 's|^#define LUA_ROOT\t"/usr/local/"|#define LUA_ROOT\t"%{_prefix}/"|' src/luaconf.h

%build
cd src

%{__cc} %{optflags} -fPIC -DLUA_USE_LINUX -c \
  lapi.c lcode.c lctype.c ldebug.c ldo.c ldump.c lfunc.c lgc.c llex.c \
  lmem.c lobject.c lopcodes.c lparser.c lstate.c lstring.c ltable.c ltm.c \
  lundump.c lvm.c lzio.c lauxlib.c lbaselib.c lcorolib.c ldblib.c liolib.c \
  lmathlib.c loadlib.c loslib.c lstrlib.c ltablib.c lutf8lib.c linit.c

%{__cc} %{build_ldflags} -shared -Wl,-soname,liblua%{major_version}.so.%{major_version} \
  -o liblua%{major_version}.so.%{version} *.o -lm -ldl

%install
install -Dm0755 src/liblua%{major_version}.so.%{version} \
  %{buildroot}%{_libdir}/liblua%{major_version}.so.%{version}

ln -s liblua%{major_version}.so.%{version} %{buildroot}%{_libdir}/liblua%{major_version}.so.%{major_version}
ln -s liblua%{major_version}.so.%{version} %{buildroot}%{_libdir}/liblua%{major_version}.so

install -d %{buildroot}%{_includedir}/lua%{major_version}

for header in lua.h luaconf.h lualib.h lauxlib.h lua.hpp; do
  install -m0644 src/$header %{buildroot}%{_includedir}/lua%{major_version}/
done

install -d %{buildroot}%{_libdir}/pkgconfig

cat > %{buildroot}%{_libdir}/pkgconfig/lua%{major_version}.pc <<EOF
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/lua%{major_version}

Name: Lua
Description: An extensible extension language (%{major_version})
Version: %{version}
Libs: -L\${libdir} -llua%{major_version} -lm -ldl
Cflags: -I\${includedir}
EOF

%files
%license doc/readme.html
%{_libdir}/liblua%{major_version}.so.%{major_version}
%{_libdir}/liblua%{major_version}.so.%{version}

%files devel
%{_includedir}/lua%{major_version}/
%{_libdir}/liblua%{major_version}.so
%{_libdir}/pkgconfig/lua%{major_version}.pc

%changelog
%autochangelog
