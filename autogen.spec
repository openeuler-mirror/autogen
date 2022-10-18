Name:		autogen
Version:	5.18.16
Release:	3
License:	GPLv2+ and GPLv3+
Summary:	Automated text file generator
URL:		http://www.gnu.org/software/autogen/
Provides:	autogen-libopts
Obsoletes:	autogen-libopts
Source0:	http://ftp.gnu.org/gnu/autogen/rel%{version}/%{name}-%{version}.tar.xz

Patch0:	backport-fix-stray-blanking-of-config-file-char.patch

BuildRequires:	gcc guile-devel libtool libxml2-devel
BuildRequires:	perl-generators
BuildRequires:  chrpath

%description
AutoGen is a tool designed to simplify the creation and maintenance of
programs that contain large amounts of repetitious text. It is especially
valuable in programs that have several blocks of text that must be kept
synchronised.

%package	devel
Summary:        Development files for autogen
License:	LGPLv3+

Requires:	automake autogen pkgconfig
Provides:	autogen-libopts-devel
Provides:	pkgconfig(autoopts)
Obsoletes:	autogen-libopts-devel

%description    devel
This package contains development files for autogen.

%package	help
Summary:	Documents for autogen
Buildarch:	noarch
Requires:	man

%description    help
Man pages and other related documents.

%prep
%autosetup -n %{name}-%{version} -p1

%build
# Static libraries are needed to run test-suite.
export CFLAGS="$RPM_OPT_FLAGS -Wno-implicit-fallthrough -Wno-format-overflow \
		-Wno-format-truncation"
%configure

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' ./libtool

%make_build

%check
make check

%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT

#Remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/{columns,getdefs,%{name},xml2ag}

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

%delete_la_and_a


%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO pkg/libopts/COPYING.gplv3 pkg/libopts/COPYING.mbsd pkg/libopts/COPYING.lgplv3
%{_bindir}/columns
%{_bindir}/getdefs
%{_bindir}/%{name}
%{_bindir}/xml2ag
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_libdir}/libopts.so.25*
%config(noreplace) /etc/ld.so.conf.d/*

%files devel
%{_bindir}/autoopts-config
%{_datadir}/aclocal/autoopts.m4
%{_libdir}/libopts.so
%{_libdir}/pkgconfig/autoopts.pc
%dir %{_includedir}/autoopts
%{_includedir}/autoopts/options.h
%{_includedir}/autoopts/usage-txt.h

%files help
%{_mandir}/man1/autoopts-config.1.gz
%{_mandir}/man3/*
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/columns.1.gz
%{_mandir}/man1/getdefs.1.gz
%{_mandir}/man1/xml2ag.1.gz
%{_infodir}/%{name}.info*.gz
%exclude %{_infodir}/dir

%changelog
* Tue Oct 18 2022 zhangruifang <zhangruifang1@h-partners.com> - 5.18.16-3
- fix stray blanking of config file char

* Thu Jul 28 2022 zoulin <zoulin13@h-partners.com> - 5.18.16-2
- remove rpath and runpath of exec files and libraries

* Thu Jul 16 2020 wangchen <wangchen137@huawei.com> - 5.18.16-1
- Update to 5.18.16

* Mon Dec 30 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.18.14-4
- Modify Source

* Thu Aug 29 2019 hexiaowen <hexiaowen@huawei.com> - 5.18.14-3
- Package init
