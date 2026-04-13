# netfusion.routeros

An Ansible collection for MikroTik RouterOS automation in the NetFusion environment.

This collection currently focuses on two areas:

* provisioning RouterOS devices for monitoring with an `mktxp` service account
* deploying the `mktxp` Prometheus exporter on a monitoring host

## Included roles

### mikrotik_mktxp_user

Creates and maintains the RouterOS group and user used by `mktxp`, and ensures the RouterOS API service is enabled on the expected port.

What it manages:

* monitoring group on MikroTik devices
* monitoring user on MikroTik devices
* allowed-address restriction for the monitoring user
* RouterOS API service port and enabled state

### mktxp_exporter

Installs `mktxp` on a monitoring host, renders `mktxp.conf`, and manages the systemd service.

What it manages:

* local `mktxp` system user and group
* Python virtual environment
* `mktxp` package installation
* `/etc/mktxp/mktxp.conf`
* `mktxp.service`

## Collection structure

collections/ansible_collections/netfusion/routeros/

* galaxy.yml
* README.md
* playbooks/

  * mikrotik_mktxp.yml
  * nft_monitor_mktxp.yml
* roles/

  * mikrotik_mktxp_user/
  * mktxp_exporter/

## Requirements

* Ansible Core
* SSH access from the control host to MikroTik devices
* RouterOS devices with API service available for `mktxp`
* A monitoring host capable of running `mktxp`
* Inventory variables and vault secrets populated for your environment

## Inventory expectations

This collection was built around an inventory structure like:

network_switches:
vars:
ansible_user: ansible
ansible_connection: network_cli
hosts:
nft-sw01:
ansible_host: 192.168.48.90
device_type: mikrotik

Typical variables used for RouterOS monitoring user management include:

* mktxp_group_name
* mktxp_group_policy
* mktxp_user_name
* mktxp_user_password
* mktxp_user_allowed_address
* mktxp_api_service
* mktxp_api_port

Typical variables used for exporter deployment include:

* mktxp_router_group
* mktxp_router_username
* mktxp_router_password
* mktxp_listen_host
* mktxp_listen_port
* mktxp_custom_labels_default

## Example playbooks

### Configure MikroTik switches

* name: Create MKTXP group and user on MikroTik devices
  hosts: network_switches
  gather_facts: false
  collections:

  * netfusion.routeros

  roles:

  * role: netfusion.routeros.mikrotik_mktxp_user

### Deploy MKTXP on monitoring host

* name: Install and configure MKTXP on nft-monitor
  hosts: nft-monitor
  become: true
  gather_facts: true
  collections:

  * netfusion.routeros

  roles:

  * role: netfusion.routeros.mktxp_exporter

## Example commands

Configure reachable MikroTik switches:

ansible-playbook playbooks/mikrotik_mktxp.yml --limit nft-sw01,nft-sw04,nft-sw05

Deploy exporter to monitoring host:

ansible-playbook playbooks/nft_monitor_mktxp.yml --limit nft-monitor

## Notes

* RouterOS user allowed-address restrictions must match the real source IP of the monitoring host.
* Prometheus should target the real listening address of the monitoring host, not an assumed address.
* Unreachable devices can be disabled in exporter config generation with host vars such as `mktxp_enabled: false`.

## License

MIT
