# NOTE:
# - the plugin's feature to check plugin freshness compares mtime of shared libs provided on project homepage:
#   static void skype_plugin_update_check(void)
#        basename = g_path_get_basename(this_plugin->path);
#        purple_util_fetch_url(g_strconcat("http://eion.robbmob.com/version?version=", basename, NULL),
#   which could be largely bogus depending when we build our package, touch
#   *.so after build with reference of source files? source tarball?
%define		svnrev	628
Summary:	Skype API Plugin for Pidgin/libpurple/Adium
Name:		libpurple-protocol-skype
Version:	20120215
Release:	1
License:	GPL v3
Group:		Applications/Communications
Source0:	skype4pidgin-r%{svnrev}.tar.bz2
# Source0-md5:	0196b4674d07b53c36fda78c3e9be685
Source1:	get-source.sh
URL:		http://code.google.com/p/skype4pidgin/
BuildRequires:	gettext-devel
BuildRequires:	glib-devel
BuildRequires:	libpurple-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
Requires:	skype-program
Provides:	libpurple-protocol
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Skype Plugin for Pidgin/libpurple/Adium. It lets you view
and chat with all your Skype buddies from within Pidgin/Adium. You
still need Skype to be running to be able to use it, but it lets you
keep a consistent user interface and use all the other nifty
Pidgin/Adium plugins with it, like spell-checking or OTR encryption.

%prep
%setup -qn skype4pidgin-r%{svnrev}
%{__sed} -i -e 's,\r$,,' README.txt
%{__sed} -i -e 's,-g -march=athlon-xp -O2 -pipe,$(CFLAGS),' Makefile
%{__sed} -i -e 's,-g -pipe,$(CFLAGS),' Makefile
%{__sed} -i -e 's,-g -march=athlon-xp -pipe,$(CFLAGS),' Makefile
%{__sed} -i -e 's,gcc,$(CC),' Makefile
%{__sed} -i -e 's,/usr/lib/purple-2,%{_libdir}/purple-2,' Makefile
# we want libfoo.so, not libfoo64.so, so pretend we're always building 32bit lib
%{__sed} -i -e 's,${LINUX32_COMPILER},$(CC),' Makefile

# yes it is weird place to find version date, because he this time forgot to update changelog
version=$(awk -F'"' '/define PRODUCT_VERSION/{print $2}' skype4pidgin.nsi)
if [ "[$version]" != "[$(date '+%d-%b-%Y' -d %{version})]" ]; then
	:
#	exit 1
fi

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
%{_pixmapsdir}/pidgin/protocols/*/skype.png
%{_pixmapsdir}/pidgin/protocols/*/skypeout.png
