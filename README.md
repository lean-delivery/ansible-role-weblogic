weblogic
=========
[![License](https://img.shields.io/badge/license-Apache-green.svg?style=flat)](https://raw.githubusercontent.com/lean-delivery/ansible-role-weblogic/master/LICENSE)
[![Build Status](https://travis-ci.org/lean-delivery/ansible-role-weblogic.svg?branch=master)](https://travis-ci.org/lean-delivery/ansible-role-weblogic)
[![Build Status](https://gitlab.com/lean-delivery/ansible-role-weblogic/badges/master/build.svg)](https://gitlab.com/lean-delivery/ansible-role-weblogic)

## Summary
--------------

This role installs Oracle WebLogic Server on Linux platforms which allows to build and deploy enterprise Java EE applications.


Requirements
--------------

 - Minimal Version of the ansible for installation: 2.5
 - **Supported Weblogic versions**:
   - 10.x
   - 12.1.x
   - 12.2.1.x
   - _higher versions should be retested_
 - **Supported OS**:
   - CentOS
     - 6
     - 7

For more information regarding support matrix please visit <https://support.oracle.com>

Java should be installed preliminarily:
  - lean_delivery.java

For running "java -jar" opensource module `javax` was used (https://github.com/tima/ansible-javax)

```
For test scenarios weblogic/requirements.yml is used  
If another roles/versions are required, put requirements.yml to molecule/<scenario_name> and remove in molecule.yml lines  
  options:  
    role-file: requirements.yml
```


Role Variables
--------------

  - `transport` - artifact source transport  
     available:
      - `web` - fetch artifact from custom web uri
      - `local` - local artifact

  - `transport_web` - URI for http/https artifact  e.g. "http://my-storage.example.com/V886423-01.zip"
  - `transport_local` - path for local artifact e.g. "/tmp/V886423-01.zip"

  - `download_path` - local folder for downloading artifacts  
    default: `/tmp`

  - `wls_user` - user for installing Oracle WebLogic  
    default: `weblogic`
  - `wls_group` - group for weblogic user  
    default: `weblogic`

  - `wls_version` - Oracle WebLogic version

#### Set WebLogic version as it's defined in official Oracle Documentation

  - `wls_path` - where WebLogic should be installed  
    default: `/opt/weblogic`

#### Parameters for creating Node Manager

##### To install Node Manager
```yaml
node_manager:
  install: True
  port: "5556"
  service: "wls-nodemanager"
```

##### To skip Node Manager installation
```yaml
node_manager:
  install: False
```

#### Parameters for creating WebLogic domain

##### To install WebLogic Domain with Development mode without SSL
```yaml
domain:
  create: True
  name: "base_domain"
  server: "AdminServer"
  service: "wls-admin-server"
  user: "weblogic"
  password: "welcome0"
  port: "7001"
  start_mode: "dev"
  ssl: False
```

##### To install WebLogic Domain with Development mode with SSL
```yaml
domain:
  create: True
  name: "base_domain"
  server: "AdminServer"
  service: "wls-admin-server"
  user: "weblogic"
  password: "welcome0"
  port: "7001"
  start_mode: "dev"
  ssl: True
  ssl_port: "7002"
```

##### To skip Domain installation

```yaml
domain:
  create: False
```


#### Parameters for WebLogic versions starting from 12.1.2

  - `install_type` - installation type, based on installation executor (jar) file  
    available:  
      - `WebLogic Server`
      - `Complete with Examples`
      - `Coherence`
      - `Fusion Middleware Infrastructure`
      - `Fusion Middleware Infrastructure With Examples`

  - `install_group` - install group for user  
    default: `oinstall`

  - `inventory_directory` - path to oracle inventory directory  
    default: `/opt/oraInventory`

  - `ora_inst` - path to oraInst.loc file  
    default: `/etc/oraInst.loc`

##### Swap configuration

  - `swapfile_path` - path to swap file  
    default: `/swapfile`

  - `swapfile_bs_size_mb`  
    default: `1`

  - `swapfile_count` - swap size  
    default: `514`


Example Playbook
----------------

### Installing WebLogic 12.2.1.3.0 from local:
```yaml
- name: "Install WebLogic 12.2.1.3.0 from local"
  hosts: all

  roles:
    - role: lean_delivery.java
      java_major_version: 8
      java_minor_version: 181
    - role: lean_delivery.weblogic
      wls_version: "12.2.1.3.0"
      transport: "local"
      transport_local: "/tmp/V886423-01.zip"
      install_type: "WebLogic Server"
```

### Installing WebLogic 10.3.6 with SSL from web:
```yaml
- name: "Install WebLogic 10.3.6 with SSL from web"
  hosts: all

  roles:
    - role: lean_delivery.java
      java_major_version: 6
      java_minor_version: 45
      transport: "web"
      transport_web: "http://my-storage.example.com/jdk-6u45-linux-x64.tar.gz"
    - role: lean_delivery.weblogic
      wls_version: "10.3.6"
      transport: "web"
      transport_web: "http://my-storage.example.com/V29852-01.zip"
      domain:
        create: True
        name: "base_domain"
        server: "AdminServer"
        service: "wls-admin-server"
        user: "weblogic"
        password: "welcome0"
        port: "7001"
        start_mode: "dev"
        ssl: True
        ssl_port: "7002"
```


## License

[Apache License 2.0](https://raw.githubusercontent.com/lean-delivery/ansible-role-weblogic/master/LICENSE)

## Authors

[Lean Delivery team](team@lean-delivery.com)
