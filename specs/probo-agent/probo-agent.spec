%global debug_package %{nil}

Name:           probo-agent
Version:        0.8.0
Release:        1%{?dist}
Summary:        Probo device posture agent
License:        MIT
URL:            https://github.com/getprobo/probo
Source0:        %{url}/releases/download/probo-agent/v%{version}/probo-agent_Linux_x86_64.tar.gz#/probo-agent-%{version}.Linux_x86_64.tar.gz
Source1:        probo-agent.service
Source2:        probo-agent.sysusers
ExclusiveArch:  x86_64

BuildRequires:  systemd-rpm-macros

%description
probo-agent runs as a managed OS service, reporting device posture to Probo.

This package repackages the official upstream binary release and runs the
agent as the unprivileged probo user. Self-update is not possible, updates
are delivered through this repository; enroll with --no-auto-update and
--skip-service, then enable probo-agent.service.

%prep
%setup -q -n probo-agent_Linux_x86_64

%install
install -Dm0755 probo-agent %{buildroot}%{_bindir}/probo-agent
install -Dm0644 %{SOURCE1} %{buildroot}%{_unitdir}/probo-agent.service
install -Dm0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/probo-agent.conf
install -dm0700 %{buildroot}%{_sharedstatedir}/probo-agent

%check
./probo-agent --version | grep -F '%{version}'

%post
%systemd_post probo-agent.service

%preun
%systemd_preun probo-agent.service

%postun
%systemd_postun_with_restart probo-agent.service

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/probo-agent
%{_unitdir}/probo-agent.service
%{_sysusersdir}/probo-agent.conf
%dir %attr(0700,probo,probo) %{_sharedstatedir}/probo-agent

%changelog
%autochangelog
