%define debug_package %{nil}

%global gh_user jc21

Name:           dnsrouter
Version:        0.0.6
Release:        1%{?dist}
Summary:        Simple DNS daemon to redirect requests based on domain names
Group:          Applications/System
License:        MIT
URL:            https://github.com/%{gh_user}/%{name}
Source0:        https://github.com/%{gh_user}/%{name}/archive/v%{version}.tar.gz
Source1:        %{name}.service
BuildRequires:  git golang systemd-rpm-macros

%description
A simplistic dns daemon that you can use as your local DNS server
and have it route DNS requests to upstream servers based on the
requested domain.

%prep
%setup -q -n %{name}-%{version}

%build
go build \
	-ldflags "-linkmode=external -w -s -X main.commit=$(git rev-parse --short HEAD) -X main.version=$(cat .version)" \
	-o "%{_builddir}/bin/%{name}" \
	./cmd/%{name}

%install
install -Dm0755 %{_builddir}/bin/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/%{name}.service

%files
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%post
%{_bindir}/%{name} -w -c /etc/dnsrouter/config.json
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Wed Oct 27 2021 Jamie Curnow <jc@jc21.com> 0.0.6-1
- https://github.com/jc21/dnsrouter/releases/tag/v0.0.6

* Mon Jun 28 2021 Jamie Curnow <jc@jc21.com> 0.0.4-1
- https://github.com/jc21/dnsrouter/releases/tag/v0.0.4

* Fri Jun 25 2021 Jamie Curnow <jc@jc21.com> 0.0.3-1
- https://github.com/jc21/dnsrouter/releases/tag/v0.0.3

