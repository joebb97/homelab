# JUNIPER ANSIBLE IS A MESS

juniper.device ports over junipernetworks.junos.junos_*
functionality, but adds its own modules on top of it. command (juniper.device.command), config (juniper.device.config), facts, etc. These only work with connection: local or connection: pyez

connection: local is being deprecated,
if connection: local is used then you don't need ansible_network_os

connection: local is the equivalent of specifying ansible_connection: local

juniper pyez connection doesn't work with any of the junos_* modules, i.e junos_vlans, junos_interfaces

connection: netconf works with NETCONF over SSH but needs ansible_network_os: junos .

juniper pyez requires you to set 

    # host: "{{ inventory_hostname }}"
    # user: root

as variables somewhere. connection: local doesn't reqire user.

I'm sticking with NETCONF over SSH.

junos_command is for read-only commands I guess? junos_config is for general config updates

junos_command

```
- name: Get configuration
  juniper.device.junos_command:
    commands:
      - show configuration
    display: set
```

The `show` commands seem to not work with junos_config. Gives netconf xml errors

I think only juniper_command works with ansible.netcommon.network_cli but doesn't support writes. If you're using network_cli you're better off just using ansible.netcommon.cli_config

## juniper making an irb

first need to do 
  set interfaces irb unit <num>

then you need to do
  set vlans <vlan-name> l3-interface irb.<num>

in that order. if you try `set vlans ...` first it will fail if the irb interface hasn't been made

<num> in both cases has to be the same
but the actual vlan-id associated with <vlan-name> can be different than <num>. you're really supposed to set them to be the same, but it's not enforced. why is it not enforced? why juniper? why????

this does let you bump the vlan id independently of the irb unit number, e.g in a different commit. then you can do junos_vlans -> junos_l3_interfaces
