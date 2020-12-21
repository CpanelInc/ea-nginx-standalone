Name:           ea-nginx-standalone
Version:        1.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4552 for more details
%define release_prefix 1
Release:        %{release_prefix}%{?dist}.cpanel
Summary:        Enable standalone config for ea-nginx
License:        GPL
Group:          System Environment/Libraries
URL:            http://www.cpanel.net
Vendor:         cPanel, Inc.
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:       ea-nginx

Source0:        enable.standalone

%description
By default ea-nginx proxies all requests to Apache and acts as a caching layer.
This package changes that to have nginx handle static content, passenger apps,
 and proxy everything else to other things including cpsrvd, Apache, and FPM.

**Caution**: While this may be more performant keep in mind that no .htaccess
 or Apache restrictions will be in effect which is a security problem
 if you rely on them.

%build
echo "Nothing to build"

%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}/etc/nginx/ea-nginx/
install %{SOURCE0} %{buildroot}/etc/nginx/ea-nginx/enable.standalone

%clean
rm -rf %{buildroot}

%posttrans
/usr/local/cpanel/scripts/ea-nginx config --all

%files
%defattr(0644,root,root,0755)
/etc/nginx/ea-nginx/enable.standalone

%changelog
* Mon Dec 21 2020 Daniel Muey <dan@cpanel.net> - 1.0-1
- ZC-8054: Initial version

