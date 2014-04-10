#
# spec file for package samba (Version 4.1.0)
#
# Copyright (c) 2007 Suman Manjunath
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2014 Zentyal S.L., http://www.zentyal.com
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Author(s):
#   Kamen Mazdrashki <kmazdrashki@zentyal.com>
#

# norootforbuild

%define sambaprefix		/opt/samba4

%define _prefix		%{sambaprefix}
%define _sysconfdir 	%{sambaprefix}/etc
%define _localstatedir	%{sambaprefix}/var
%define _local_bindir   %{sambaprefix}/bin
%define _local_sbindir  %{sambaprefix}/sbin
%define _local_libdir   %{sambaprefix}/lib
%define _local_datadir  %{sambaprefix}/share
%define _local_includedir %{sambaprefix}/include

Name:           samba4
Version:        4.1.4
Release:        1.0
Summary:        Samba 4
License:        GPL v3 only
Group:          Productivity/Networking/Samba
Source:         http://ftp.samba.org/pub/samba/samba-%{version}.tar.gz
#Patch0:         vfs_full_audit.diff
Url:            http://www.samba.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  pkgconfig
#BuildRequires:  gnutls-devel pam-devel popt-devel python-devel readline-devel sqlite3-devel libacl-devel
BuildRequires:  lib64gnutls-devel lib64pam-devel lib64popt-devel lib64python-devel lib64readline-devel lib64acl-devel
Requires:       python >= 2.5, perl
AutoReqProv:    on
Provides:       samba4 = %{version}
Obsoletes:      samba4 < %{version}, samba-client, samba-common, samba-doc, samba-domainjoin-gui, samba-server, samba-swat
Obsoletes:      samba-virusfilter-clamav, samba-virusfilter-fsecure, samba-virusfilter-sophos, samba-winbind

%description
Samba 4 beta built so that it does not interfere with system.

Authors:
--------
    The Samba Team <samba@samba.org>

%package devel
License:        GPL v3 only
Summary:        Samba 4
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Requires:       gnutls-devel pam-devel popt-devel python-devel readline-devel sqlite3-devel

%description devel
Samba 4 beta built so that it does not interfere with system.

Authors:
--------
    The Samba Team <samba@samba.org>

%prep
%setup -q -n samba-%{version}
#%patch0 -p1 
%{__rm} -rf %{buildroot}

%build
  CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
  CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
  FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \
  %{_configure} --host=%{_host} --build=%{_build} \
        --prefix=%{_prefix} 
#        --program-prefix=%{?_program_prefix} \
#        --disable-dependency-tracking \
#        --prefix=%{_prefix} \
#        --exec-prefix=%{_exec_prefix} \
#        --bindir=%{_bindir} \
#        --sbindir=%{_sbindir} \
#        --sysconfdir=%{_sysconfdir} \
#        --datadir=%{_datadir} \
#        --includedir=%{_includedir} \
#        --libdir=%{_libdir} \
#        --libexecdir=%{_libexecdir} \
#        --localstatedir=%{_localstatedir} \
#        --sharedstatedir=%{_sharedstatedir} \
#        --mandir=%{_mandir} \
#        --infodir=%{_infodir}
# clear 'no-undefined' linked flags here until we find a way to this in configure
sed -i -e "s|, '-Wl,--no-undefined'||g" bin/c4che/default.cache.py
%__make %{?jobs:-j%jobs}

%install
%{make_install}
%__mkdir_p %{buildroot}%{_localstatedir}/run
%__mkdir_p %{buildroot}%{_localstatedir}/lib
%__mkdir_p %{buildroot}/etc/ld.so.conf.d/


%__mkdir_p %{buildroot}/%{_prefix}/etc/
%__mkdir_p %{buildroot}/%{_prefix}/private/

# symlink samba/sbin
%__mkdir_p %{buildroot}/%{_sbindir}/
%__ln_s %{buildroot}/%{_local_sbindir}/nmbd %{buildroot}/%{_sbindir}/
%__ln_s %{buildroot}/%{_local_sbindir}/samba %{buildroot}/%{_sbindir}/
%__ln_s %{buildroot}/%{_local_sbindir}/samba_dnsupdate %{buildroot}/%{_sbindir}/
%__ln_s %{buildroot}/%{_local_sbindir}/samba_kcc %{buildroot}/%{_sbindir}/
%__ln_s %{buildroot}/%{_local_sbindir}/samba_spnupdate %{buildroot}/%{_sbindir}/
%__ln_s %{buildroot}/%{_local_sbindir}/samba_upgradedns %{buildroot}/%{_sbindir}/
%__ln_s %{buildroot}/%{_local_sbindir}/smbd %{buildroot}/%{_sbindir}/
%__ln_s %{buildroot}/%{_local_sbindir}/winbindd %{buildroot}/%{_sbindir}/

%__mkdir_p %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/cifsdd %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/dbwrap_tool %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/eventlogadm %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/gentest %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ldbadd %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ldbdel %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ldbedit %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ldbmodify %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ldbrename %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ldbsearch %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/locktest %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/masktest %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ndrdump %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/net %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/nmblookup %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/nmblookup4 %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ntdbbackup %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ntdbdump %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ntdbrestore %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ntdbtool %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/ntlm_auth %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/oLschema2ldif %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/pdbedit %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/pidl %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/profiles %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/regdiff %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/regpatch %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/regshell %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/regtree %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/rpcclient %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/samba-tool %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/sharesec %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbcacls %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbclient %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbclient4 %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbcontrol %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbcquotas %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbget %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbpasswd %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbspool %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbstatus %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbtar %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbta-util %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbtorture %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/smbtree %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/tdbbackup %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/tdbdump %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/tdbrestore %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/tdbtool %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/testparm %{buildroot}/%{_bindir}/
%__ln_s %{buildroot}/%{_local_bindir}/wbinfo %{buildroot}/%{_bindir}/


%post
/sbin/ldconfig
echo '#!/bin/sh
#
# chkconfig: 35 91 9
# description: Starts and stops the Samba samba daemon \
#	       used to provide SMB network services.
#
### BEGIN INIT INFO
# Provides:       samba4
# Required-Start: $network $remote_fs $syslog
# Should-Start:   
# Required-Stop:  $network $remote_fs $syslog
# Should-Stop:    
# Default-Start:  3 4 5
# Default-Stop:   0 1 2 6
# Short-Description: Samba server (samba)
# Description:Starts and stops the Samba samba daemons used to provide SMB network
#             services.
### END INIT INFO

SMBD_BIN="/opt/samba4/sbin/samba"
SMB_CONF="/opt/samba4/etc/smb.conf"
PID_FILE="/opt/samba4/var/run/samba.pid"

# Source function library.
if [ -f /etc/init.d/functions ] ; then
  . /etc/init.d/functions
elif [ -f /etc/rc.d/init.d/functions ] ; then
  . /etc/rc.d/init.d/functions
else
  exit 0
fi

# Source networking configuration.
. /etc/sysconfig/network

# Check that networking is up.
[ ${NETWORKING} = "no" ] && exit 0

# Check that smb.conf exists.
[ -f ${SMB_CONF} ] || exit 0

# Check for missing binary
if [ ! -x ${SMBD_BIN} ]; then
	echo -n >&2 "Samba SMB daemon, ${SMBD_BIN} is not installed. "
	rc_status -s
	exit 5
fi

RETVAL=0

# be extra carefull cause connection fail if TMPDIR is not writeable
export TMPDIR="/var/tmp"

start() {
	export TMPDIR="/var/tmp"
	echo -n "Starting Samba SMB daemon "
	gprintf "Starting Samba4: "
	daemon -p ${PID_FILE} ${SMBD_BIN} -D -s ${SMB_CONF}
	RETVAL=$?
	echo
	[ $RETVAL -eq 0 ] && touch /var/lock/subsys/samba
	return $RETVAL
}
stop() {
	gprintf "Shutting down Samba4: "
	killproc -p ${PID_FILE} -t 10 ${SMBD_BIN}
	RETVAL=$?
	echo
	[ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/samba
	return $RETVAL
}
restart() {
	stop
	start
}
reload() {
	export TMPDIR="/var/tmp"
	gprintf "Reloading smb.conf file: "
	killproc -p ${PID_FILE} ${SMBD_BIN} -HUP
	RETVAL=$?
	echo
	return $RETVAL
}
mdkstatus() {
	status -p ${PID_FILE} ${SMBD_BIN}
}


case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		restart
		;;
	reload)
		reload
		;;
	status)
		mdkstatus
		;;
	condrestart)
		[ -f /var/lock/subsys/samba ] && restart || :
		;;
	*)
		gprintf "Usage: %s {start|stop|restart|status|condrestart}\n" "$0"
		exit 1
esac

exit $?
' > /etc/rc.d/init.d/samba4

chmod +x /etc/init.d/samba4


%postun
/sbin/ldconfig
rm -f /etc/rc.d/init.d/samba4


%clean
#%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
#%config /etc/ld.so.conf.d/samba4.conf
%dir %{_prefix}
%{_prefix}/etc
%{_prefix}/private
%{_local_bindir}
%{_local_sbindir}
%{_bindir}
%{_sbindir}
%dir %{_local_libdir}
%{_local_libdir}/auth
%{_local_libdir}/bind9
%{_local_libdir}/gensec
%{_local_libdir}/idmap
%{_local_libdir}/ldb
%{_local_libdir}/private
%{_local_libdir}/process_model
%{_local_libdir}64/python2.7
%{_local_libdir}/security
%{_local_libdir}/service
%{_local_libdir}/vfs
%{_local_libdir}/*.so.*
%{_localstatedir}
%{_local_datadir}
#%{_mandir}

%files devel
%defattr(-,root,root)
%{_local_includedir}
%{_local_libdir}/*.so
%dir %{_local_libdir}/nss_info
%{_local_libdir}/nss_info/*.so
%{_local_libdir}/pkgconfig

%changelog
