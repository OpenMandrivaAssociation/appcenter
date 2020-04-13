Name:           appcenter
Version:        3.2.4
Release:        1
Summary:        An open, pay-what-you-want app store for indie developers
License:        GPL-3.0
Group:          System/Configuration
URL:            https://elementary.io/
Source:         https://github.com/elementary/appcenter/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: appstream
BuildRequires: appstream-vala
BuildRequires: cmake
BuildRequires: fdupes
BuildRequires: gettext
BuildRequires: gettext-devel
BuildRequires: meson
BuildRequires: pkgconfig
#BuildRequires: update-desktop-files
BuildRequires: pkgconfig(appstream)
BuildRequires: pkgconfig(appstream-glib)
BuildRequires: pkgconfig(flatpak)
BuildRequires: pkgconfig(gee-0.8)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(granite)
BuildRequires: pkgconfig(gthread-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libhandy-0.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(libsoup-2.4)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(packagekit-glib2)
BuildRequires: pkgconfig(vapigen)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: libxml2-utils

Recommends:     %{name}-lang
Provides:       appcenter = %{version}

%description
AppCenter is a native Gtk+ app store built on AppStream and Packagekit.

%package -n     gnome-shell-search-provider-appcenter
Summary:        Browse and manage apps -- Search Provider for GNOME Shell
Group:          System/GUI/GNOME
Requires:       %{name} = %{version}
Requires:       gnome-shell

%description -n gnome-shell-search-provider-appcenter
AppCenter is a native Gtk+ app store built on AppStream and Packagekit.

This package contains a search provider to enable GNOME Shell to get search
results from AppCenter.

%lang_package

%prep
%setup -q

# Use the system logo
sed -i 's/\(distributor\)-logo/\1/' $(grep -rwl distributor-logo)

%build
%meson	\
    -Dcurated=false \
    -Dhomepage=false \
    -Dlibunity=false \
    -Dpayments=false
%meson_build

%install
%meson_install
#%find_lang io.elementary.appcenter %{name}.lang

# Add .desktop file to autostart
install -Dm0644 \
  %{buildroot}%{_datadir}/applications/io.elementary.appcenter-daemon.desktop \
  %{buildroot}%{_sysconfdir}/xdg/autostart/io.elementary.appcenter-daemon.desktop

# Add OnlyShowIn key
#if ! grep OnlyShowIn.*Pantheon %{buildroot}%{_datadir}/applications/io.elementary.appcenter-daemon.desktop; then
#	sed -i '$aOnlyShowIn=Pantheon;' %{buildroot}%{_sysconfdir}/xdg/autostart/io.elementary.appcenter-daemon.desktop
#else
#	'This entry already exists' 2> /dev/null
#fi

%files
%license COPYING
%doc README.md
%{_bindir}/io.elementary.appcenter
%{_datadir}/applications/io.elementary.appcenter*.desktop
#{_datadir}/dbus-1/services/io.elementary.appcenter.service
%{_datadir}/glib-2.0/schemas/io.elementary.appcenter.gschema.xml
%{_datadir}/metainfo/io.elementary.appcenter.appdata.xml
%{_datadir}/locale/*/LC_MESSAGES/io.elementary.appcenter.mo
%dir %{_sysconfdir}/io.elementary.appcenter
%config %{_sysconfdir}/io.elementary.appcenter/appcenter.blacklist
%{_sysconfdir}/xdg/autostart/io.elementary.appcenter-daemon.desktop

%files -n gnome-shell-search-provider-appcenter
%dir %{_datadir}/gnome-shell
%dir %{_datadir}/gnome-shell/search-providers
%{_datadir}/gnome-shell/search-providers/io.elementary.appcenter.search-provider.ini

#%files lang -f %{name}.lang
