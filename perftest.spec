Name:		perftest
Summary:	IB Performance Tests
Version:	3.0
%define		tar_release 3.1.gb36a595
Release:	7%{?dist}
License:	GPLv2 or BSD
Group:		Productivity/Networking/Diagnostic
Source0:	https://www.openfabrics.org/downloads/%{name}/%{name}-%{version}-%{tar_release}.tar.gz
Source1:	ib_atomic_bw.1
Patch0:		perftest-3.0-cflags.patch
Patch1:		perftest-enable-s390x-platform-support.patch
Patch2:		perftest-3.0-fix-memory-leaks.patch
Url:		http://www.openfabrics.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libibverbs-devel > 1.1.4, librdmacm-devel > 1.0.14
BuildRequires:	libibumad-devel > 1.3.6
BuildRequires:	autoconf, automake, libtool
Obsoletes:	openib-perftest < 1.3

%description
Perftest is a collection of simple test programs designed to utilize 
RDMA communications and provide performance numbers over those RDMA
connections.  It does not work on normal TCP/IP networks, only on
RDMA networks.

%prep
%setup -q
%patch0 -p1 -b .cflags
%patch1 -p1
%patch2 -p1
autoreconf --force --install

%build
%configure
make V=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
for file in ib_{atomic,read,send,write}_{lat,bw}; do
	install -D -m 0755 $file %{buildroot}%{_bindir}/$file
done
for file in raw_ethernet_{lat,bw}; do
	install -D -m 0755 $file %{buildroot}%{_bindir}/$file
done
mkdir -p %{buildroot}%{_mandir}/man1/
install -D -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/
pushd %{buildroot}%{_mandir}/man1/
for file in ib_atomic_lat ib_{read,send,write}_{lat,bw} raw_ethernet_{lat,bw}; do
	ln -s ib_atomic_bw.1 ${file}.1
done
popd

%files
%defattr(-, root, root)
%doc README COPYING
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Thu Aug 18 2016 Jarod Wilson <jarod@redhat.com> - 3.0-7
- Address a myriad more coverity/clang warnings
- Add raw_ethernet_* man page symlinks
- Related: rhbz#1273176
- Related: rhbz#948476

* Mon Aug 15 2016 Jarod Wilson <jarod@redhat.com> - 3.0-6
- Update to upstream 3.0-3.1.gb36a595 tarball for upstream fixes
- Add in manpages
- Related: rhbz#1365750
- Resolves: rhbz#948476

* Fri Aug 12 2016 Jarod Wilson <jarod@redhat.com> - 3.0-5
- Make it possible to actually test with XRC connections again
- Resolves: rhbz#1365750

* Mon Aug 08 2016 Jarod Wilson <jarod@redhat.com> - 3.0-4
- Install raw_ethernet{lat,bw} tools
- Resolves: rhbz#1365182

* Wed May 18 2016 Jarod Wilson <jarod@redhat.com> - 3.0-3
- Fix additional memory leaks reported and spotted after last fix

* Wed May 18 2016 Jarod Wilson <jarod@redhat.com> - 3.0-2
- Fix issues uncovered by coverity

* Wed May 04 2016 Jarod Wilson <jarod@redhat.com> - 3.0-1
- Update to upstream release v3.0
- Resolves: bz1309586, bz1273176

* Tue Jun 16 2015 Michal Schmidt <mschmidt@redhat.com> - 2.4-1
- Update to latest upstream release
- Enable s390x platform
- Resolves: bz1182177

* Fri Oct 17 2014 Doug Ledford <dledford@redhat.com> - 2.3-1
- Update to latest upstream release
- Resolves: bz1061582

* Tue May 20 2014 Kyle McMartin <kmcmarti@redhat.com> - 2.0-4
- aarch64: add get_cycles implementation since <asm/timex.h> is no longer
  exported by the kernel.
- Resolves: #1100043

* Thu Jan 23 2014 Doug Ledford <dledford@redhat.com> - 2.0-3
- Fix for rpmdiff found issues
- Related: bz1017321

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0-2
- Mass rebuild 2013-12-27

* Wed Jul 17 2013 Doug Ledford <dledford@redhat.com> - 2.0-1
- Update to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 06 2012 Doug Ledford <dledford@redhat.com> - 1.3.0-2
- Update to latest upstream release
- Initial import into Fedora
- Remove runme from docs section (review item)
- Improve description of package (review item)

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

