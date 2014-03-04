# Mandriva Project

Samba/OpenChange modules for MBS

## Resources and Bibliography

* Wiki start: [http://projects.mandriva.org/projects/mmc/wiki/Start]
* MDS development mailing-list archives: [https://lists.mandriva.com/wws/arc/mds-devel/]
* MDS development: [http://projects.mandriva.org/projects/mmc/wiki/MDS\_Development]
* MMC development: [http://mandriva-management-console.readthedocs.org/en/latest/]

### Core development resources
* [http://mandriva-management-console.readthedocs.org/en/latest/devel/python-module.html]
* [http://mandriva-management-console.readthedocs.org/en/latest/devel/php-module.html]

# Mandriva MBS module 

Mandriva MBS is the SMB Mandriva product. From a global perspective, it is similar to Zentyal. It provides a Linux distribution with a web-based configuration and administration interface and integrates a mechanism of plugins to extend the capabilities of the default installation. Their applications/modules are however distributed through an application store, similar to Apple, Google, or Samsung store.

# Architecture 

## General Overview 

The MBS product is architectured around LDAP. It is the link between modules and it powers Mandriva module integration, primarily between user/groups, mail and samba.



1. The core distribution is installed through a graphical interface
2. The mandriva server setup (MSS) is installing and configuring the core modules (shipped by default). It is done through a specific web interface running on **https://IP:8000**
3. The dashboard - MMC Agent is running on `https://IP` and provide service management and post-install configurations



The components used to currently deploy Samba3 module in Mandriva are:

1. **mmc-web-samba** <span style="font-size: 12px;">: SAMBA module for the MMC web interface</span>
2. **python-mmc-samba** <span style="font-size: 12px;">: Mandriva Management Console SAMBA plugin</span>

# Implementation 

## Backend - Python module 

* **Runs on 127.0.0.1:7080**

Mandriva provides a python based application called mmc-agent. It is powered by Django framework and listens for XML-RPC requests. These requests are turned into actions and the application implements backend code such as modification of configuration file, service management (start/stop/restart/reload), services actions, etc.

`python /usr/sbin/mmc-agent`

* configuration file: `/etc/mmc/agent/config.ini`

* log file: `/var/log/mmc/mmc-agent.log`

* python class file: `/usr/lib/python2.7/site-packages/mmc/agent.py`

This service is responsible for loading the plugins (PluginManager).

* This is an internal class which just looks into the directory where plugins are installed and look for `__init__.py` for each of them:

`/usr/lib/python2.7/site-packages/mmc/plugins/*/__init__.py`

* It runs the `loadPlugins()` method which will call the `activate()` method from the plugin

<pre>
DEBUG   Trying to load module samba4
DEBUG   Module samba4 loaded
INFO    Plugin samba4 loaded, version: 1.0.0
</pre>


## Frontend: PHP 

## Samba4 

Samba4 is not packaged as part of MBS 1.0 but is available as a package for mageia cauldron ([https://wiki.mageia.org/en/Cauldron](https://wiki.mageia.org/en/Cauldron)) and available at the following URL:

[http://svnweb.mageia.org/packages/cauldron/samba4/](http://svnweb.mageia.org/packages/cauldron/samba4/)

