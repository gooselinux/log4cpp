Name:           log4cpp
Version:        1.0
Release:        13%{?dist}
Summary:        C++ logging library

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://sourceforge.net/projects/log4cpp/
Source0:        http://downloads.sourceforge.net/log4cpp/%{name}-%{version}.tar.gz
# Fix errors when compiling with gcc >= 4.3
Patch0:         log4cpp-1.0-gcc43.patch
# Don't put build cflags in .pc
Patch1:         log4cpp-1.0-remove-pc-cflags.patch
# Install docs into DESTDIR
Patch2:         log4cpp-1.0-fix-doc-dest.patch
# Don't try to build snprintf.c
Patch3:         log4cpp-1.0-no-snprintf.patch
# Remove date from html/api footers (as they cause a multi-arch problem)
Patch4:         log4cpp-1.0-remove-date-from-html-footer.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

ExclusiveArch:  x86_64 i686

BuildRequires:  gcc-c++
BuildRequires:  doxygen
BuildRequires:  automake, autoconf, libtool

Obsoletes: %{name}-docs < 1.0-13

%description
A library of C++ classes for flexible logging to files, syslog, IDSA and
other destinations. It is modeled after the Log for Java library
(http://www.log4j.org), staying as close to their API as is reasonable.

%package devel
Summary:        Header files, libraries and development documentation for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q
%patch0 -p 1 -b .gcc43
%patch1 -p 1 -b .no-cflags
%patch2 -p 1 -b .doc-dest
%patch3 -p1 -b .no-snprintf
%patch4 -p1 -b .remove-date-from-html-footer

# Delete non-free (but freely distributable) file under Artistic 1.0
# just to be sure we're not using it.
rm -rf src/snprintf.c
iconv -f iso-8859-1 -t utf8 -o THANKS.utf8 THANKS
iconv -f iso-8859-1 -t utf8 -o ChangeLog.utf8 ChangeLog
mv THANKS.utf8 THANKS
mv ChangeLog.utf8 ChangeLog

%build
aclocal -I m4
autoconf
autoheader
automake --add-missing --copy
libtoolize --copy --force
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# rpmlint complains (twice) about installdox, and there is no need for it
# as all the docs are already installed
%{__rm} %{buildroot}/usr/share/doc/log4cpp-%{version}/api/installdox

%{__mv} %{buildroot}/usr/share/doc/log4cpp-%{version} rpmdocs

# fix multi-arch/multilib issues, rename log4cpp-config according to it's arch
%{__mv} %{buildroot}/%{_bindir}/log4cpp-config{,-%{_arch}}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README THANKS TODO rpmdocs/*
%doc %{_mandir}/man3/log4cpp*
%{_libdir}/liblog4cpp.so.*

%files devel
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README THANKS TODO
%{_bindir}/log4cpp-config-%{_arch}
%{_includedir}/log4cpp/
%{_libdir}/liblog4cpp.so
%{_libdir}/pkgconfig/log4cpp.pc
%{_datadir}/aclocal/log4cpp.m4
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la


%changelog
* Mon Apr 26 2010 Uri Lublin <uril@redhat.com> - 1.0-13.el6
  Fix review comments:
    - Remove -doc sub-package
Related: #555835

* Mon Apr 26 2010 Uri Lublin <uril@redhat.com> - 1.0-12.el6
  Fixed multi-lib/multi-arch issues:
    - Remove date from html-footer (doc/html/api/*)
    - Also in preparation of removing -doc subpackage
Related: #555835

* Wed Apr 14 2010 Uri Lublin <uril@redhat.com> - 1.0-11.el6
  Fix review comments:
    - removed installdox from -docs sub-package
    - fixed multi-lib/multi-arch issues
      - renamed log4cpp-config according to arch
Related: #555835

* Fri Jan 29 2010 Uri Lublin <uril@redhat.com> - 1.0-10.el6
  Fix rpmlint issues:
    - Added doc files to -devel subpackage
    - Made doc-file api/installdox non-executable
Related: #555835

* Mon Jan 25 2010 Uri Lublin <uril@redhat.com> - 1.0-9.el6
  ExclusiveArch:  x86_64 i686 (Replaced i386 with i686).
Resolves: #558473

* Thu Jan 14 2010 Uri Lublin <uril@redhat.com> - 1.0-8.el6
  Copy changes done by Tom "spot" Callaway <tcallawa@redhat.com> in Fedora-12:
  - Delete non-free (but freely distributable) snprintf.c under Artistic 1.0
  Copy changes done by Yuval Kashtan <ykashtan@redhat.com> in RHEL-5:
  -   Create a -docs subpackage to resolve a multilib conflict. (502679)
  -   Convert some files from iso-8859-1 to utf8 (makes rpmlint happy).
  -   ExclusiveArch:  x86_64 i386 (513407)
Related: #549888

* Wed Jan 13 2010 Yuval Kashtan <ykashtan@redhat.com> - 1.0-6.el5
- fix multilib conflict in log4cpp-1.0-3.el5

* Tue Jan 05 2010 Yuval Kashtan <ykashtan@redhat.com> - 1.0-5.el5
- add i386, for qspice-xpi, to fix "log4cpp is not built for i386"

* Mon Jul 27 2009 Yuval Kashtan <ykashtan@redhat.com> - 1.0-4.el5
- limit rpm to x86_64, because it is used only by qspice, to fix
  "stack smashing detected" error on ia64 (513407)

* Thu May 21 2009 Yuval Kashtan <ykashtan@redhat.com> - 1.0-3.el5
- fix log4cpp needs rebuild to increase version number to be greater than version
  used in RHEVH branch (502047)

* Thu Apr 16 2009 Yuval Kashtan <ykashtan@redhat.com> - 1.0-1.el5
- rpmlint issues (convert to utf8) (488608)

* Mon Feb  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-2.fc12
- Delete non-free (but freely distributable) snprintf.c under Artistic 1.0
  just to be sure we're not using it.

* Fri Dec 12 2008 Jon McCann <jmccann@redhat.com> - 1.0-1.fc12
- Initial package
