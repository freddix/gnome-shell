Summary:	Window manager and application launcher for GNOME
Name:		gnome-shell
Version:	3.12.0
Release:	1
License:	GPL v2+
Group:		X11/Window Managers
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-shell/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	8071e8531e82b8e56eedf57e65179594
Source1:	%{name}-nm-libexecdir.patch
URL:		http://live.gnome.org/GnomeShell
BuildRequires:	NetworkManager-applet-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	caribou-devel
BuildRequires:	clutter-devel >= 1.18.0
BuildRequires:	dbus-glib-devel
BuildRequires:	evolution-data-server-devel >= 3.12.0
BuildRequires:	folks-devel >= 0.9.6
BuildRequires:	gcr-devel >= 3.12.0
BuildRequires:	gettext-devel
BuildRequires:	gjs-devel >= 1.40.0
BuildRequires:	gnome-bluetooth-devel >= 3.12.0
BuildRequires:	gnome-control-center-devel >= 3.12.0
BuildRequires:	gnome-desktop-devel >= 3.12.0
BuildRequires:	gnome-menus-devel
BuildRequires:	gobject-introspection-devel >= 1.40.0
BuildRequires:	gsettings-desktop-schemas-devel >= 3.12.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.2
BuildRequires:	gtk+3-devel >= 3.12.0
BuildRequires:	intltool
BuildRequires:	json-glib-devel
BuildRequires:	libcanberra-devel
BuildRequires:	libcroco-devel
BuildRequires:	libgnome-keyring-devel >= 3.12.0
BuildRequires:	libsoup-devel >= 2.46.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	mutter-devel >= 3.12.0
BuildRequires:	pkg-config
BuildRequires:	polkit-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	startup-notification-devel
BuildRequires:	systemd-devel
BuildRequires:	telepathy-glib-devel
BuildRequires:	telepathy-logger-devel
Requires(post,postun):	glib-gio-gsettings
# g-is nm-gtk
Requires:	NetworkManager-applet-libs
Requires:	accountsservice
Requires:	at-spi2-atk
Requires:	caribou
Requires:	evolution-data-server >= 3.12.0
Requires:	gjs >= 1.40.0
Requires:	gnome-control-center >= 3.12.0
Requires:	gnome-menus
Requires:	gsettings-desktop-schemas >= 3.12.0
Requires:	mutter >= 3.12.0
Requires:	nautilus >= 3.12.0
Requires:	telepathy-logger
Requires:	telepathy-mission-control
Requires:	telepathy-service
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
GNOME Shell is the defining technology of the GNOME 3 desktop user
experience. It provides core interface functions like switching to
windows and launching applications. GNOME Shell takes advantage of the
capabilities of modern graphics hardware and introduces innovative
user interface concepts to provide a delightful and easy to use
experience.

%package apidocs
Summary:	GNOME Shell API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
This package provides GNOME Shell API documentation.

%package -n browser-plugin-%{name}
Summary:	gnome-shell plugin for WWW browsers
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n browser-plugin-%{name}
gnome-shell plugin for WWW browsers.

%prep
%setup -q

%{__sed} "s|LIBDIR|%{_libdir}|" %{SOURCE1} | %{__patch} -p1

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--with-ca-certificates=/etc/certs/ca-certificates.crt	\
	--with-html-dir=%{_gtkdocdir}	\
	--with-systemd
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/gnome-shell/{extensions,modes,search-providers}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	mozillalibdir=%{_libdir}/browser-plugins

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gnome-shell/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache

%postun
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gnome-shell
%attr(755,root,root) %{_bindir}/gnome-shell-extension-prefs
%attr(755,root,root) %{_bindir}/gnome-shell-extension-tool
%attr(755,root,root) %{_bindir}/gnome-shell-perf-tool

%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/gnome-shell-calendar-server
%attr(755,root,root) %{_libexecdir}/gnome-shell-hotplug-sniffer
%attr(755,root,root) %{_libexecdir}/gnome-shell-perf-helper

%attr(755,root,root) %{_libdir}/gnome-shell/libgnome-shell-js.so
%attr(755,root,root) %{_libdir}/gnome-shell/libgnome-shell-menu.so
%attr(755,root,root) %{_libdir}/gnome-shell/libgnome-shell.so
%{_libdir}/gnome-shell/Gvc-1.0.typelib
%{_libdir}/gnome-shell/Shell-0.1.typelib
%{_libdir}/gnome-shell/ShellJS-0.1.typelib
%{_libdir}/gnome-shell/ShellMenu-0.1.typelib
%{_libdir}/gnome-shell/St-1.0.typelib

%{_datadir}/dbus-1/interfaces/org.gnome.Shell.Screencast.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.Screenshot.xml
%{_datadir}/dbus-1/interfaces/org.gnome.ShellSearchProvider.xml
%{_datadir}/dbus-1/interfaces/org.gnome.ShellSearchProvider2.xml
%{_datadir}/dbus-1/services/org.gnome.Shell.CalendarServer.service
%{_datadir}/dbus-1/services/org.gnome.Shell.HotplugSniffer.service

%{_datadir}/gnome-control-center/keybindings/50-gnome-shell-system.xml

%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.xml

%dir %{_datadir}/gnome-shell
%{_datadir}/gnome-shell/theme
%{_datadir}/gnome-shell/modes
%{_datadir}/gnome-shell/extensions
%{_datadir}/gnome-shell/search-providers

%{_desktopdir}/evolution-calendar.desktop
%{_desktopdir}/gnome-shell-extension-prefs.desktop
%{_desktopdir}/gnome-shell.desktop
%{_mandir}/man1/gnome-shell.1*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/shell
%{_gtkdocdir}/st

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/browser-plugins/libgnome-shell-browser-plugin.so

