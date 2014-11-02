Name:       ohm-plugins-misc
Summary:    A miscallaneous set of Nokia OHM plugins
Version:    1.1.60
Release:    1
Group:      System/Resource Policy
License:    LGPLv2.1
URL:        https://github.com/nemomobile/ohm-plugins-misc
Source0:    %{name}-%{version}.tar.gz
Source1:    ohm-session-agent.service
Source2:    ohm-session-agent.conf
Source100:  ohm-plugins-misc.yaml
Patch2:     disable-x11-configure-checks.patch
Patch3:     0001-packaging-Make-building-gconf-plugin-optional.patch
Requires:   ohm
Requires:   systemd
Requires:   systemd-user-session-targets
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(check)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(bluez)
BuildRequires:  pkgconfig(libresource)
BuildRequires:  pkgconfig(ohm)
BuildRequires:  pkgconfig(libdres)
BuildRequires:  pkgconfig(profile)
BuildRequires:  bison
BuildRequires:  flex

%description
A miscallaneous set of OHM plugins by Nokia.

%package -n ohm-plugin-console
Summary:    Console OHM plugin
Group:      Development/Tools

%description -n ohm-plugin-console
OHM console plugin for debug interface.


%package -n ohm-plugin-fmradio
Summary:    FM radio enforcement point for OHM
Group:      System/Resource Policy
Requires:   %{name} = %{version}-%{release}
Requires:   ohm

%description -n ohm-plugin-fmradio
OHM fmradio plugin provides policy enforcement point for |
FM Radio.


%package -n ohm-plugin-dspep
Summary:    DSP enforcement point for OHM
Group:      System/Resource Policy
Requires:   %{name} = %{version}-%{release}
Requires:   ohm
Requires:   ohm-plugin-signaling

%description -n ohm-plugin-dspep
OHM dspep plugin provides policy enforcement point for |
DSP.


%package -n ohm-plugins-dbus
Summary:    DBus plugins for OHM
Group:      System/Resource Policy
Requires:   %{name} = %{version}-%{release}
Requires:   ohm

%description -n ohm-plugins-dbus
DBus related plugins for OHM.

%package -n ohm-plugin-telephony
Summary:    Telephony plugin for OHM
Group:      System/Resource Policy
Requires:   %{name} = %{version}-%{release}
Requires:   ohm

%description -n ohm-plugin-telephony
OHM telephony plugin provides policy control points for telephony.


%package -n ohm-plugin-signaling
Summary:    Signaling plugin for OHM
Group:      System/Resource Policy
Requires:   %{name} = %{version}-%{release}

%description -n ohm-plugin-signaling
OHM signaling plugin provides functionality required by videoep |
and dspep.


%package -n ohm-plugin-media
Summary:    Media playback enforcement point for OHM
Group:      System/Resource Policy
Requires:   %{name} = %{version}-%{release}
Requires:   ohm

%description -n ohm-plugin-media
OHM media plugin provides policy enforcement point for |
media playback.


%package -n ohm-plugin-accessories
Summary:    Sensor OHM plugin for device accessories
Group:      System/Resource Policy
Requires:   %{name} = %{version}-%{release}
Requires:   ohm

%description -n ohm-plugin-accessories
OHM accessories plugin provides functionality to detect plugged |
in device accessories.


%package -n ohm-plugin-profile
Summary:    OHM plugin for profile
Group:      System/Resource Policy
Requires:   %{name} = %{version}-%{release}
Requires:   ohm

%description -n ohm-plugin-profile
OHM profile plugin provides functionality to detect profile changes.


%prep
%setup -q -n %{name}-%{version}

# disable-x11-configure-checks.patch
%patch2 -p1
# 0001-packaging-Make-building-gconf-plugin-optional.patch
%patch3 -p1

%build
%autogen --disable-static
%configure --disable-static \
    --enable-telephony \
    --disable-notification

make

%install
rm -rf %{buildroot}
%make_install

# FIXME: install maemo-specific files distro-conditionally
rm -f -- $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xsession.post/55ohm-session-agent
rm -f -- $RPM_BUILD_ROOT%{_libdir}/ohm/*.la
rm -f -- $RPM_BUILD_ROOT%{_libdir}/ohm/libohm_call_test.so
rm -f -- $RPM_BUILD_ROOT%{_datadir}/ohm-session-agent/start-session-agent.sh

install -d %{buildroot}%{_sysconfdir}/dbus-1/session.d
install -d %{buildroot}%{_libdir}/systemd/user
install -m 644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/user
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/dbus-1/session.d
mkdir -p %{buildroot}%{_libdir}/systemd/user/pre-user-session.target.wants
ln -s ../ohm-session-agent.service %{buildroot}%{_libdir}/systemd/user/pre-user-session.target.wants/

%post
if [ "$1" -ge 1 ]; then
systemctl-user daemon-reload || :
systemctl-user restart ohm-session-agent.service || :
fi

%postun
if [ "$1" -eq 0 ]; then
systemctl-user stop ohm-session-agent.service || :
systemctl-user daemon-reload || :
fi

%files
%defattr(-,root,root,-)
%{_libdir}/ohm/libohm_auth.so
%{_libdir}/ohm/libohm_auth_test.so
%{_libdir}/ohm/libohm_delay.so
%{_libdir}/ohm/libohm_resource.so
%{_bindir}/ohm-session-agent
%config %{_sysconfdir}/ohm/plugins.d/auth.ini
%config %{_sysconfdir}/ohm/plugins.d/resource.ini
%{_sysconfdir}/dbus-1/session.d/*.conf
%{_libdir}/systemd/user/*.service
%{_libdir}/systemd/user/pre-user-session.target.wants/ohm-session-agent.service
%doc README COPYING AUTHORS

%files -n ohm-plugin-console
%defattr(-,root,root,-)
%{_libdir}/ohm/libohm_console.so
%doc COPYING AUTHORS

%files -n ohm-plugin-fmradio
%defattr(-,root,root,-)
%{_libdir}/ohm/libohm_fmradio.so

%files -n ohm-plugin-dspep
%defattr(-,root,root,-)
%{_libdir}/ohm/libohm_dspep.so

%files -n ohm-plugins-dbus
%defattr(-,root,root,-)
%{_libdir}/ohm/libohm_dbus.so
%{_libdir}/ohm/libohm_dbus_signal.so

%files -n ohm-plugin-telephony
%defattr(-,root,root,-)
%{_libdir}/ohm/libohm_telephony.so

%files -n ohm-plugin-signaling
%defattr(-,root,root,-)
%{_libdir}/ohm/libohm_signaling.so

%files -n ohm-plugin-media
%defattr(-,root,root,-)
%{_libdir}/ohm/libohm_media.so
%config %{_sysconfdir}/ohm/plugins.d/media.ini

%files -n ohm-plugin-accessories
%defattr(-,root,root,-)
%{_libdir}/ohm/libohm_accessories.so

%files -n ohm-plugin-profile
%defattr(-,root,root,-)
%{_libdir}/ohm/libohm_profile.so

