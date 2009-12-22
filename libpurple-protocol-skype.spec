Summary:	Skype API Plugin for Pidgin/libpurple/Adium
Name:		libpurple-protocol-skype
Version:	0.1
Release:	0.2
License:	GPL v3
Group:		Applications/Communications
# svn checkout http://skype4pidgin.googlecode.com/svn/trunk/ skype4pidgin
# tar --exclude=.svn -cjf skype4pidgin-r$(svnversion skype4pidgin).tar.bz2 skype4pidgin
Source0:	skype4pidgin-r558.tar.bz2
# Source0-md5:	bde82b7df7dd5f7afaa90e023dc77668
URL:		http://code.google.com/p/skype4pidgin/
BuildRequires:	glib2-devel
BuildRequires:	pidgin-devel
BuildRequires:	sed >= 4.0
Requires:	skype
Provides:	libpurple-protocol
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Skype Plugin for Pidgin/libpurple/Adium. It lets you view
and chat with all your Skype buddies from within Pidgin/Adium. You
still need Skype to be running to be able to use it, but it lets you
keep a consistent user interface and use all the other nifty
Pidgin/Adium plugins with it, like spell-checking or OTR encryption.

%prep
%setup -q -n skype4pidgin
%{__sed} -i -e 's,\r$,,' README.txt
%{__sed} -i -e 's,-g -march=athlon-xp -O2 -pipe,$(CFLAGS),' Makefile
%{__sed} -i -e 's,-g -O2 -pipe,$(CFLAGS),' Makefile
%{__sed} -i -e 's,gcc,$(CC),' Makefile
%{__sed} -i -e 's,/usr/lib/purple-2,%{_libdir}/purple-2,' Makefile
# we want libfoo.so, not libfoo64.so, so pretend we're always building 32bit lib
%{__sed} -i -e 's,${LINUX32_COMPILER},$(CC),' Makefile

%build
%{__make} \
	libskype_dbus.so all \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"
	LIBPURPLE_CFLAGS="$(pkg-config --cflags purple)" \
	GLIB_CFLAGS="$(pkg-config --cflags glib)" \
	DBUS_CFLAGS="$(pkg-config --cflags dbus-glib-1)" \

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt COPYING.txt README.txt TODO.txt
%attr(755,root,root) %{_libdir}/purple-2/libskype.so
%attr(755,root,root) %{_libdir}/purple-2/libskype_dbus.so
%dir %{_pixmapsdir}/pidgin/emotes/skype
%{_pixmapsdir}/pidgin/emotes/skype/theme
%{_pixmapsdir}/pidgin/protocols/16/skype.png
%{_pixmapsdir}/pidgin/protocols/16/skypeout.png
%{_pixmapsdir}/pidgin/protocols/22/skype.png
%{_pixmapsdir}/pidgin/protocols/22/skypeout.png
%{_pixmapsdir}/pidgin/protocols/48/skype.png
%{_pixmapsdir}/pidgin/protocols/48/skypeout.png
