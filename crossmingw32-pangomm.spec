Summary:	A C++ interface for pango library - cross MinGW32 version
Summary(pl.UTF-8):	Interfejs C++ dla biblioteki pango - wersja skrośna MinGW32
Name:		crossmingw32-pangomm
Version:	2.26.3
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pangomm/2.26/pangomm-%{version}.tar.bz2
# Source0-md5:	1f2712d53918cfb4745c291a67b86156
URL:		http://www.gtkmm.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	crossmingw32-cairomm >= 1.6.3
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-glibmm >= 2.22.0
BuildRequires:	crossmingw32-pango >= 1.24.0
BuildRequires:	libtool >= 2:1.5
BuildRequires:	mm-common
BuildRequires:	pkgconfig >= 1:0.15
Requires:	crossmingw32-cairomm >= 1.6.3
Requires:	crossmingw32-glibmm >= 2.16.0
Requires:	crossmingw32-pango >= 1.24.0
Provides:	crossmingw32-gtkmm-pango
Obsoletes:	crossmingw32-gtkmm-pango
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
A C++ interface for pango library - cross MinGW32 version.

%description -l pl.UTF-8
Interfejs C++ dla biblioteki pango - wersja skrośna MinGW32.

%package static
Summary:	Static pangomm library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka pangomm (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	crossmingw32-gtkmm-pango-static
Obsoletes:	crossmingw32-gtkmm-pango-static

%description static
Static pangomm library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka pangomm (wersja skrośna MinGW32).

%package dll
Summary:	DLL pangomm library for Windows
Summary(pl.UTF-8):	Biblioteka DLL pangomm dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-cairomm-dll >= 1.6.3
Requires:	crossmingw32-glibmm-dll >= 2.16.0
Requires:	crossmingw32-pango-dll >= 1.24.0
Requires:	wine
Provides:	crossmingw32-gtkmm-pango-dll
Obsoletes:	crossmingw32-gtkmm-pango-dll

%description dll
DLL pangomm library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL pangomm dla Windows.

%prep
%setup -q -n pangomm-%{version}

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-documentation \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libpangomm-1.4.dll.a
%{_libdir}/libpangomm-1.4.la
%{_libdir}/pangomm-1.4
%{_includedir}/pangomm-1.4
%{_pkgconfigdir}/pangomm-1.4.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpangomm-1.4.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libpangomm-1.4-*.dll
