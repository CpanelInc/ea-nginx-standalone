Name:           ea-nginx-standalone
Version:        1.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4552 for more details
%define release_prefix 3
Release:        %{release_prefix}%{?dist}.cpanel
Summary:        Enable standalone config for ea-nginx
License:        GPL
Group:          System Environment/Libraries
URL:            http://www.cpanel.net
Vendor:         cPanel, Inc.
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:       ea-nginx
Requires:       ea-nginx-passenger

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

%post

# record the current value of fileprotect
# if this is a new install
if [ $1 -eq 1 ]; then
    if [ -e /var/cpanel/fileprotect ]; then
        touch /etc/nginx/ea-nginx/meta/fileprotect
    else
        rm -f /etc/nginx/ea-nginx/meta/fileprotect
    fi

    # disable file protect
    /usr/local/cpanel/bin/whmapi1 set_tweaksetting key=enablefileprotect value=0
fi

%posttrans
/usr/local/cpanel/scripts/ea-nginx config --all

%preun

if [ $1 -eq 0 ]; then
    if [ -e /etc/nginx/ea-nginx/meta/fileprotect ]; then
        rm -f /etc/nginx/ea-nginx/meta/fileprotect
        /usr/local/cpanel/bin/whmapi1 set_tweaksetting key=enablefileprotect value=1
    fi
fi

%files
%defattr(0644,root,root,0755)
/etc/nginx/ea-nginx/enable.standalone

%changelog
* Mon Oct 02 2023 Travis Holloway <t.holloway@cpanel.net> - 1.0-3
- EA-11530: Disable file protect when in standalone mode

* Wed Jul 12 2023 Brian Mendoza <brian.mendoza@cpanel.net> - 1.0-2
- ZC-10396: Add ea-nginx-passenger dependency

* Mon Dec 21 2020 Daniel Muey <dan@cpanel.net> - 1.0-1
- ZC-8054: Initial version

