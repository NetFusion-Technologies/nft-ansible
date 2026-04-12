# netfusion.sysalerts

Reusable collection for:

- Postfix relay setup
- sysalerts sender/recipient rewriting
- subject tagging
- hostname suffix standardization

## Role

### `netfusion.sysalerts.postfix_relay`

Configures Debian-family hosts to:

- relay mail through `mail.netfusiontechnologies.com:587`
- authenticate as `sysalerts@netfusiontechnologies.com`
- rewrite local recipients to `sysalerts@netfusiontechnologies.com`
- rewrite sender to `sysalerts@netfusiontechnologies.com`
- tag message subjects with `[hostname][service]`

## Variables

See `roles/postfix_relay/defaults/main.yml`.

## Example playbook

```yaml
- name: Deploy sysalerts relay
  hosts: managed_linux:!bluestar
  become: true
  gather_facts: true
  roles:
    - role: netfusion.sysalerts.postfix_relay

