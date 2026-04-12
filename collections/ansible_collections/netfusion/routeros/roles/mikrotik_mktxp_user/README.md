Creates a least-privilege RouterOS group and user for mktxp/Prometheus scraping.

Expected inventory for RouterOS devices should already provide SSH/CLI connectivity for Ansible, for example:

ansible_connection: ansible.netcommon.network_cli
ansible_network_os: community.network.routeros
ansible_user: ansible
ansible_password: "{{ vault_routeros_ansible_password }}"
