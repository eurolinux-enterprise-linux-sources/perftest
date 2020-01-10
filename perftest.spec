Name:		perftest
Summary:	IB Performance Tests
Version:	3.0
Release:	2.0.16.gb2f2e82%{?dist}
License:	GPLv2 or BSD
Group:		Productivity/Networking/Diagnostic
Source:		https://www.openfabrics.org/downloads/perftest/%{name}-%{version}-0.16.gb2f2e82.tar.gz
Patch0:		perftest-2.0-cflags.patch
Url:		http://www.openfabrics.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libibverbs-devel > 1.1.7, librdmacm-devel > 1.0.17
BuildRequires:	libibumad-devel > 1.3.8
BuildRequires:	libtool, automake, autoconf
Obsoletes:	openib-perftest <= 1.2
ExcludeArch:	s390 s390x

%description
Perftest is a collection of simple test programs designed to utilize 
RDMA communications and provide performance numbers over those RDMA
connections.  It does not work on normal TCP/IP networks, only on
RDMA networks.

%prep
%setup -q
%patch0 -p1
# Upstream tarball has source files marked executable.
chmod -x src/*.[ch]

%build
%configure
make %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

# Several programs were obsoleted by the upgrade from 1.3 to 2.0
# Create symlinks from the old program name to the most appropriate
# replacement program so, hopefully, scripts and such won't stop
# working suddenly.  However, there is no guarantee that changes to
# allowed options won't trip some scripts up.
ln -s ib_read_lat %{buildroot}%{_bindir}/rdma_lat
ln -s ib_read_bw %{buildroot}%{_bindir}/rdma_bw
ln -s ib_write_bw %{buildroot}%{_bindir}/ib_write_bw_postlist

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README COPYING runme
%_bindir/*

%changelog
* Thu Jan 21 2016 Michal Schmidt <mschmidt@redhat.com> - 3.0-2.0.16.gb2f2e82
- Respect distro CFLAGS, restore fortification.
- debuginfo package had executable source files.
- Related: bz1127235, bz1129312

* Tue Jan 19 2016 Michal Schmidt <mschmidt@redhat.com> - 3.0-1.0.16.gb2f2e82
- Update to latest upstream release
- Related: bz1127235, bz1129312

* Wed Jun 18 2014 Doug Ledford <dledford@redhat.com> - 2.2-1
- Update to latest upstream release
- Related: bz830099

* Tue Sep 03 2013 Doug Ledford <dledford@redhat.com> - 2.0-2
- Fix rpmdiff detected error.  Upstream overrode our cflags so stack
  protector got turned off.
- Related: bz806183

* Thu Aug 01 2013 Doug Ledford <dledford@redhat.com> - 2.0-1
- Update to latest upstream release
- We had to drop ib_clock_test program as no equivalent exists
  in the latest release
- Resolves: bz806183, bz806185, bz830099

* Tue Jan 31 2012 Doug Ledford <dledford@redhat.com> - 1.3.0-2
- Update to latest upstream release
- No longer strip rocee related code out, we can compile with it now
- Related: bz739138

* Fri Jul 22 2011 Doug Ledford <dledford@redhat.com> - 1.3.0-1
- Update to latest upstream release (1.2.3 -> 1.3.0)
- Strip rocee related code out of upstream update
- Add a buildrequires on libibumad because upstream needs it now
- Fix lack of build on i686
- Related: bz725016
- Resolves: bz724896

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.2.3-3.el6
- More minor pkgwrangler cleanups
- Related: bz543948

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.2.3-2.el6
- Fixes for pkgwrangler review
- Related: bz543948

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 1.2.3-1.el5
- Update to latest upstream version
- Related: bz518218

* Mon Jun 22 2009 Doug Ledford <dledford@redhat.com> - 1.2-14.el5
- Rebuild against libibverbs that isn't missing the proper ppc wmb() macro
- Related: bz506258

* Sun Jun 21 2009 Doug Ledford <dledford@redhat.com> - 1.2-13.el5
- Update to ofed 1.4.1 final bits
- Rebuild against non-XRC libibverbs
- Related: bz506097, bz506258

* Sat Apr 18 2009 Doug Ledford <dledford@redhat.com> - 1.2-12.el5
- Update to ofed 1.4.1-rc3 version
- Remove dead patch
- Related: bz459652

* Wed Sep 17 2008 Doug Ledford <dledford@redhat.com> - 1.2-11
- Upstream has updated the tarball without updating the version, so we
  grabbed the one from the OFED-1.3.2-20080728.0355 tarball
- Resolves: bz451481

* Wed Apr 09 2008 Doug Ledford <dledford@redhat.com> - 1.2-10
- Fix the fact that the itc clock on ia64 may be a multiple of the cpu clock
- Resolves: bz433659

* Tue Apr 01 2008 Doug Ledford <dledford@redhat.com> - 1.2-9
- Update to OFED 1.3 final bits
- Related: bz428197

* Sun Jan 27 2008 Doug Ledford <dledford@redhat.com> - 1.2-8
- Split out to separate package (used to be part of openib package)
- Related: bz428197

