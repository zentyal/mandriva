#
# spec file for package samba (Version 4.1.0)
#
# Copyright (c) 2007 Suman Manjunath
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

%define sambaprefix		/opt/samba4

%define _prefix		%{sambaprefix}
%define _sysconfdir 	%{sambaprefix}/etc
%define _localstatedir	%{sambaprefix}/var

Name:           samba4
Version:        4.1.4
Release:        5.1
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

%build
%configure --prefix=%{_prefix}
%__make %{?jobs:-j%jobs}

%install
%{makeinstall}
%__mkdir_p %{buildroot}%{_localstatedir}/run
%__mkdir_p %{buildroot}%{_localstatedir}/lib
%__mkdir_p %{buildroot}/etc/ld.so.conf.d/
#echo %{_libdir} > %{buildroot}/etc/ld.so.conf.d/samba4.conf
#echo %{_libdir}/private >> %{buildroot}/etc/ld.so.conf.d/samba4.conf

%__mkdir_p %{buildroot}/%{_prefix}/etc/
%__mkdir_p %{buildroot}/%{_prefix}/private/



%post
/sbin/ldconfig
echo '#! /bin/sh
# Copyright (c) 1999-2004 SuSE Linux AG, Nuernberg, Germany.
# All rights reserved.
#
# Author: Lars Mueller <lmuelle@suse.de>
#
# /etc/init.d/samba4
#   and its symbolic link
# /usr/sbin/rcsamba4
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
### BEGIN INIT INFO
# Provides:       samba4
# Required-Start: $network $remote_fs $syslog
# Should-Start:   
# Required-Stop:  $network $remote_fs $syslog
# Should-Stop:    
# Default-Start:  3 5
# Default-Stop:   0 1 2 6
# Short-Description: Samba 4 SMB/CIFS file and print server
# Description:    Samba 4 SMB/CIFS file and print server
### END INIT INFO

SMBD_BIN="/opt/samba4/sbin/samba"
SMB_CONF="/opt/samba4/etc/smb.conf"
PID_FILE="/opt/samba4/var/run/samba.pid"

. /etc/rc.status
rc_reset

# Check for missing binary
if [ ! -x ${SMBD_BIN} ]; then
	echo -n >&2 "Samba SMB daemon, ${SMBD_BIN} is not installed. "
	rc_status -s
	exit 5
fi

# be extra carefull cause connection fail if TMPDIR is not writeable
export TMPDIR="/var/tmp"

test -f /etc/sysconfig/samba && \
	. /etc/sysconfig/samba

for setting in $SAMBA_SMBD_ENV; do
	pathcheck="${setting%%:*}"
	variable="${setting##*:}"
	test "${pathcheck}" != "${variable}" -a ! -e "${pathcheck}" && \
		continue
	export eval ${variable}
done

case "$1" in
	start)
		echo -n "Starting Samba SMB daemon "
		if [ ! -f ${SMB_CONF} ]; then
			echo -n >&2 "Samba configuration file, ${SMB_CONF} does not exist. "
			rc_status -s
			exit 6
		fi
		checkproc -p ${PID_FILE} ${SMBD_BIN}
		case $? in
			0) echo -n "- Warning: daemon already running. " ;;
			1) echo -n "- Warning: ${PID_FILE} exists. " ;;
		esac
		test -f /etc/sysconfig/language && \
			. /etc/sysconfig/language
		export LC_ALL="$RC_LC_ALL"
		export LC_CTYPE="$RC_LC_CTYPE"
		export LANG="$RC_LANG"
		startproc -p ${PID_FILE} ${SMBD_BIN} -D -s ${SMB_CONF}
		unset LC_ALL LC_CTYPE LANG
		rc_status -v
		;;
	stop)
		echo -n "Shutting down Samba SMB daemon "
		checkproc -p ${PID_FILE} ${SMBD_BIN} || \
			echo -n " Warning: daemon not running. "
		killproc -p ${PID_FILE} -t 10 ${SMBD_BIN}
		rc_status -v
		;;
	try-restart|condrestart)
		if test "$1" = "condrestart"; then
			echo "${attn} Use try-restart ${done}(LSB)${attn} rather than condrestart ${warn}(RH)${norm}"
		fi
		$0 status
		if test $? = 0; then
			$0 restart
		else 
			rc_reset
		fi
		rc_status
		;;
	restart)
		$0 stop
		$0 start
		rc_status
		;;
	force-reload|reload)
		echo -n "Reloading Samba SMB daemon "
		checkproc -p ${PID_FILE} ${SMBD_BIN} && \
			touch ${PID_FILE} || \
			echo -n >&2 " Warning: daemon not running. "
		killproc -p ${PID_FILE} -HUP ${SMBD_BIN}
		rc_status -v
		;;
	status)
		echo -n "Checking for Samba SMB daemon "
		checkproc -p ${PID_FILE} ${SMBD_BIN}
		rc_status -v
		;;
	probe)
		test ${SMB_CONF} -nt ${PID_FILE} && echo reload
		;;
	*)
		echo "Usage: $0 {start|stop|status|try-restart|restart|force-reload|reload|probe}"
		exit 1
		;;
esac
rc_exit
' > /etc/init.d/samba4

chmod +x /etc/init.d/samba4


%postun
/sbin/ldconfig
#rm -f /etc/init.d/samba4


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
#%config /etc/ld.so.conf.d/samba4.conf
%dir %{_prefix}
%{_prefix}/etc
%{_prefix}/private
%{_bindir}
%{_sbindir}
%dir %{_libdir}
%{_libdir}/auth
%{_libdir}/bind9
%{_libdir}/gensec
%{_libdir}/idmap
%{_libdir}/ldb
%{_libdir}/private
%{_libdir}/process_model
%{_libdir}/python2.7
%{_libdir}/security
%{_libdir}/service
%{_libdir}/vfs
%{_libdir}/*.so.*
%{_localstatedir}
%{_datadir}
#%{_mandir}

%files devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}/*.so
%dir %{_libdir}/nss_info
%{_libdir}/nss_info/*.so
%{_libdir}/pkgconfig

%changelog
