%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
# define icons directories...
%define _iconstheme    hicolor
%define _iconsbasedir  %{_datadir}/icons/%{_iconstheme}
%define _iconsscaldir  %{_iconsbasedir}/scalable/apps

Name:		byobu
Version:	5.97
Release:	1%{?dist}
Summary:	Light-weight, configurable window manager built upon GNU screen

Group:		Applications/System
License:	GPLv3
URL:		http://launchpad.net/byobu
Source0:	http://code.launchpad.net/byobu/trunk/%{version}/+download/byobu_%{version}.orig.tar.gz
# default windows
Source1:	fedoracommon
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
%if 0%{?rhel}%{?fedora} > 5
Requires:	python >= 2.5
%else
Requires:	python26
%endif

BuildRequires:	gettext, desktop-file-utils, automake
Requires:	screen, newt, gettext, tmux

%Description
Byobu is a Japanese term for decorative, multi-panel screens that serve 
as folding room dividers. As an open source project, Byobu is an 
elegant enhancement of the otherwise functional, plain, 
practical GNU Screen. Byobu includes an enhanced profile 
and configuration utilities for the GNU screen window manager, 
such as toggle-able system status notifications.

%prep
%setup -q
# remove swap file
if [ -e "usr/bin/.byobu-status-print.swp" ]; then rm usr/bin/.byobu-status-print.swp
fi
# fix path for lib directory in scripts
for i in `find . -type f -exec grep -l {BYOBU_PREFIX}/lib/ {} \;`; do
sed -i "s#{BYOBU_PREFIX}/lib/#{BYOBU_PREFIX}/libexec/#g" $i;
done
# fix path for lib directory #2
for i in `find . -type f -exec grep -l BYOBU_PREFIX/lib {} \;`; do
sed -i "s#BYOBU_PREFIX/lib/#BYOBU_PREFIX/libexec/#g" $i;
done


# fix path for correct directory in /usr/share
sed -i "s#DOC = BYOBU_PREFIX + '/share/doc/' + PKG#DOC='%{_pkgdocdir}'#g" usr/lib/byobu/include/config.py.in

# set default fedora windows
cp -p %{SOURCE1} usr/share/byobu/windows/common

# fix path from lib to libexec by modified Makefile.am and in
sed -i "s#/lib/#/libexec/#g" usr/lib/byobu/Makefile.am
sed -i "s#/lib/#/libexec/#g" usr/lib/byobu/Makefile.in
sed -i "s#/lib/#/libexec/#g" usr/lib/byobu/include/Makefile.am
sed -i "s#/lib/#/libexec/#g" usr/lib/byobu/include/Makefile.in

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" CP="cp -p" docdir=%{_pkgdocdir} install
rm -rf %{buildroot}%{_sysconfdir}/profile.d
# remove apport which is not available in fedora
rm %{buildroot}/%{_libexecdir}/%{name}/apport
sed -i 's#status\[\"apport\"\]=0##g' %{buildroot}%{_bindir}/byobu-config
cp -p README COPYING %{buildroot}%{_pkgdocdir}
for po in po/*.po
do
    lang=${po#po/}
    lang=${lang%.po}
    mkdir -p %{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/
    msgfmt ${po} -o %{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/%{name}.mo
done
desktop-file-install usr/share/applications/%{name}.desktop --dir %{buildroot}%{_datadir}/applications

# add icon into /usr/share/icons/hicolor/scalable/apps/ from /usr/share/byobu/pixmaps/byobu.svg
mkdir -p %{buildroot}%{_iconsscaldir}
cp -p usr/share/byobu/pixmaps/byobu.svg %{buildroot}%{_iconsscaldir}

%find_lang %{name}

%clean
#rm -rf %{buildroot}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%dir %{_libexecdir}/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_pkgdocdir}
%{_iconsscaldir}/%{name}.svg
%{_pkgdocdir}/*
%{_bindir}/%{name}*
%{_bindir}/col1
%{_bindir}/ctail
%{_bindir}/wifi-status
%{_bindir}/vigpg
%if 0%{?rhel} == 5
%{_datadir}/applications/*.desktop
%else
%{_datadir}/applications/%{name}.desktop
%endif
%{_datadir}/%{name}/*
%{_mandir}/man1/%{name}*.1.gz
%{_mandir}/man1/col1.1.gz
%{_mandir}/man1/ctail.1.gz
%{_mandir}/man1/wifi-status.1.gz
%{_mandir}/man1/vigpg.1.gz
%{_libexecdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/%{name}/*

%changelog
* Sat Sep 26 2015 Liam BEGUIN <liambeguin at, gmail.com - 5.97-1
- update to 5.97
* Sat Mar 28 2015 Jan Klepek <jan.klepek at, gmail.com> - 5.92-1
- update to 5.92, fix for #1196950

* Tue Nov 11 2014 Jan Klepek <jan.klepek at, gmail.com> - 5.87-1
- update to 5.87

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.73-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 28 2014 Jan Klepek <jan.klepek at, gmail.com> - 5.73-4
- patch for issue with missing ~/.byobu/status leading to crash in byobu-config

* Thu Feb 27 2014 Jan Klepek <jan.klepek at, gmail.com> - 5.73-3
- various upstream patches

* Wed Feb 26 2014 Jan Klepek <jan.klepek at, gmail.com> - 5.73-2
- various upstream patches

* Tue Feb 18 2014 Jan Klepek <jan.klepek at, gmail.com> - 5.73-1
- Update to latest release 

* Thu Jan 9 2014 Jan Klepek <jan.klepek at, gmail.com> - 5.69-2
- added icon (#1013240)

* Wed Jan 8 2014 Jan Klepek <jan.klepek at, gmail.com> - 5.69-1
- update to latest version (#873560)
- added tmux dependency (#907267)

* Thu Dec 12 2013 Ville Skyttä <ville.skytta@iki.fi> - 5.21-7
- Install docs to %%{_pkgdocdir} where available (#993689).
- Fix bogus dates in %%changelog.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Jan Klepek <jan.klepek at, gmail.com> - 5.21-4 
- desktop file handling fixed

* Sat Aug 25 2012 Jan Klepek <jan.klepek at, gmail.com> - 5.21-3
- another fix into documentation

* Sun Aug 19 2012 Jan Klepek <jan.klepek at, gmail.com> - 5.21-2
- fixed documentation

* Sun Aug 19 2012 Jan Klepek <jan.klepek at, gmail.com> - 5.21-1
- new minor release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 08 2012 Jan Klepek <jan.klepek at, gmail.com> - 5.17-1
- update to latest version

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 15 2011 Jan Klepek <jan.klepek at, gmail.com> - 4.41-1
- update to 4.41

* Mon Aug 1 2011 Jan Klepek <jan.klepek at, gmail.com> - 4.23-1
- update to 4.23

* Sat Jul 23 2011 Jan Klepek <jan.klepek at, gmail.com> - 4.22-2
- updated to 4.22 + various bugfixes

* Sat Jul 23 2011 Jan Klepek <jan.klepek at, gmail.com> - 4.20-1
- new major release

* Sat Jan 8 2011 Jan Klepek <jan.klepek at, gmail.com> - 3.21-1
- new release

* Sat Dec 18 2010 Jan Klepek <jan.klepek at, gmail.com> - 3.20-2
- upgrade to 3.20 + some patches

* Fri Sep 3 2010 Jan Klepek <jan.klepek at, gmail.com> - 3.4-1
- upgraded to 3.4

* Thu Jun 17 2010 Jan Klepek - 2.80-1
- bugfix for BZ#595087, changed default windows selection, removed apport from toggle status notification
- upgraded to 2.80 version

* Sun May 2 2010 Jan Klepek <jan.klepek at, gmail.com> - 2.73-1
- new version released

* Wed Apr 21 2010 Jan Klepek <jan.klepek at, gmail.com> - 2.67-3
- adjusted SHARE path

* Tue Apr 20 2010 Jan Klepek <jan.klepek at, gmail.com> - 2.67-2
- adjusted path for looking for po files and removed duplicate file entry

* Fri Apr 2 2010 Jan Klepek <jan.klepek at, gmail.com> - 2.67-1
- Initial fedora RPM release
