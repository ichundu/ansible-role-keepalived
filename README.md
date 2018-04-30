Role Name: keepalived
=========

[![Build Status](https://travis-ci.org/ichundu/ansible-role-keepalived.svg?branch=master)](https://travis-ci.org/ichundu/ansible-role-keepalived)

Install and configure keepalived on Enterprise Linux (RHEL, CentOS etc.), Debian and Ubuntu systems.

Requirements
------------

None.

Role Variables
--------------

- Variables in `defaults/mail.yml`:

    Packages to install for keepalived. The `psmis` package is included because it provides the `killall` command, which is often useful for keepalived health checks using the `vrrp_script` configuration in `/etc/keepalived/keepalived.conf` file:

    ```yaml
    keepalived_packages:
      - keepalived
      - psmisc
    ```

    Apply kernel parameters via sysctl to enable `net.ipv4.ip_nonlocal_bind` and `net.ipv4.ip_nonlocal_bind` to allow programs on the server to bind to the virtual IP address.

    ```yaml
    keepalived_sysctl:
      - name: "net.ipv4.ip_nonlocal_bind"
        value: "1"
        reload: true
        sysctl_set: true
      - name: "net.ipv4.ip_forward"
        value: "1"
        reload: true
        sysctl_set: true
    ```

    The keepalived configuration file in `/etc/keepalived/keepalived.conf` is templated with block variables for each section to allow highly flexible configuration of keepalived. For example, to configure the `vrrp_instance` section declare it as follows:

    ```yaml
    keepalived_conf_vrrp_instance: |
      vrrp_instance VI_1 {
          state MASTER
          interface eth0
          virtual_router_id 51
          priority 100
          advert_int 1
          authentication {
              auth_type PASS
              auth_pass 1111
          }
          virtual_ipaddress {
              192.168.200.16
              192.168.200.17
              192.168.200.18
          }
      }
    ```

- Variables in `vars` folder:

    OS-specific variables are loaded dynamicly by this role using the [include_vars](https://docs.ansible.com/ansible/latest/modules/include_vars_module.html#include-vars-module) module:

    ```yaml
    - name: Include OS-specific variables
      include_vars:
        file: "{{ item }}"
      with_first_found:
        - "{{ ansible_os_family }}.yml"
        - main.yml
    ```

    This allows us to define different values for the `keepalived_daemon_options` variable depending on the OS distribution used. Because these OS-specific variables are declared in the `vars` directory of the role and because variables in the `vars` directory have the highest priority we use the following trick to make it possible for this variable to be overriden at the top playbook level or in group/host vars. Inside the OS-specific vars file we declare the following variable:

    ```yaml
    __keepalived_daemon_options: "-D"
    ```

    ...and use a `set_fact` task to define the `keepalived_daemon_options` variable using conditionals to check if the variable has not been defined or has a non-empty value:

    ```yaml
    - name: Define keepalived_daemon_options variable
      set_fact:
        keepalived_daemon_options: "{{ __keepalived_daemon_options }}"
      when: (keepalived_daemon_options is not defined) or
            (keepalived_daemon_options == "")
    ```

Dependencies
------------

None

Example Playbook
----------------

```yaml
- hosts: servers

  vars:
    keepalived_conf_vrrp_instance: |
      vrrp_instance VI_1 {
          state MASTER
          interface eth0
          virtual_router_id 51
          priority 100
          advert_int 1
          authentication {
              auth_type PASS
              auth_pass 1111
          }
          virtual_ipaddress {
              10.230.230.230
          }
      }

  roles:
    - ichundu.keepalived
```

License
-------

GPLv2

Author Information
------------------

https://github.com/ichundu
