# netfusion.monitoring

Reusable collection for NetFusion monitoring infrastructure.

## Scope

This collection is intended to manage:

- Prometheus
- Alertmanager
- Grafana
- Prometheus exporters
- scrape configuration
- monitoring-related defaults and service wiring

## Roles

### `netfusion.monitoring.alertmanager`
Deploys and configures Alertmanager for email-based alert routing.

### `netfusion.monitoring.prometheus_server`
Deploys and configures the Prometheus server, scrape jobs, rule files, and Alertmanager integration.

### `netfusion.monitoring.prometheus_pve_exporter`
Deploys the Proxmox VE Prometheus exporter and configures API access for Proxmox metrics collection.

### `netfusion.monitoring.grafana`
Deploys and configures Grafana, including optional use of an existing PostgreSQL or MariaDB backend.

### `netfusion.monitoring.exporters_base`
Shared tasks, defaults, or handlers for exporter-style roles.

### `netfusion.monitoring.node_exporter`
Deploys and configures node_exporter on Linux systems.

## Design goals

- Keep monitoring code separate from sysalerts/mail relay code
- Prefer inventory-driven configuration
- Reuse existing infrastructure where appropriate
- Keep Prometheus and Alertmanager on native local storage
- Use an existing database backend for Grafana when desired

## Inventory model

Typical related variables live in:

- `inventories/production/group_vars/all/main.yml`
- `inventories/production/group_vars/monitoring/main.yml`
- `inventories/production/group_vars/monitoring/vault.yml`
- `inventories/production/group_vars/proxmox_nodes/main.yml`
- `inventories/production/group_vars/proxmox_nodes/vault.yml`

## Example playbooks

### Deploy Alertmanager

- name: Deploy Alertmanager
  hosts: prometheus-alertmanager
  become: true
  gather_facts: true

  collections:
    - netfusion.monitoring

  roles:
    - alertmanager

- name: Deploy Prometheus Proxmox exporter
  hosts: proxmox_nodes
  become: true
  gather_facts: true

  collections:
    - netfusion.monitoring

  roles:
    - prometheus_pve_exporter
