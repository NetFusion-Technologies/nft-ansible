# NetFusion DNS Naming Convention

## Overview

This document defines the naming conventions for hosts, services, and applications within the NetFusion environment. The goal is to maintain clarity, consistency, and scalability while aligning DNS, infrastructure, and operational understanding.

---

## Core Principles

1. **One namespace per purpose**

   * `.net` → Internal identity (authoritative in Unbound)
   * `.xyz` → Public/admin access via reverse proxy (nginx)
   * `.com` → Client-facing services
   * `.home.arpa` → DHCP / endpoint naming
   * `.internal` → Backend / cluster communication

2. **One system = one canonical identity**

   * Every system has a single authoritative `.net` FQDN

3. **Access ≠ Identity**

   * Internal hostnames (`.net`) are not reused for public/admin access
   * Public/admin access uses separate DNS names routed through nginx

4. **Hostname alignment**

   * Short hostname = first label of FQDN = Proxmox name

---

## Naming Structure

### Host / Infrastructure

Used for physical hardware and core infrastructure devices.

Examples:

```
nft-pve1.netfusiontechnologies.net
nft-pve2.netfusiontechnologies.net
nft-monitor.netfusiontechnologies.net
nft-sw1.netfusiontechnologies.net
nft-nas1.netfusiontechnologies.net
nft-printer1.netfusiontechnologies.net
```

---

### Virtual Machines / Containers

Represents OS-level instances.

Prefix:

```
vm-
```

Examples:

```
vm-bluestar.netfusiontechnologies.net
vm-haos1.netfusiontechnologies.net
```

Optional (if distinguishing container types later):

```
ct-nginx1
```

---

### Databases

Stateful data services.

Prefix:

```
db-
```

Examples:

```
db-postgres.netfusiontechnologies.net
db-mongo.netfusiontechnologies.net
db-mariadb.netfusiontechnologies.net
```

---

### Shared Services / Platform Services

Services consumed by operators or systems.

Prefix:

```
svc-
```

Examples:

```
svc-grafana.netfusiontechnologies.net
svc-prometheus.netfusiontechnologies.net
svc-loki.netfusiontechnologies.net
svc-alertmanager.netfusiontechnologies.net
```

---

### Infrastructure Services

Core infrastructure and access-layer components.

Prefix:

```
infra-
```

Examples:

```
infra-nginx.netfusiontechnologies.net
infra-guac.netfusiontechnologies.net
infra-tomcat.netfusiontechnologies.net
```

---

### Automation Platforms

Home/building automation systems.

Prefix:

```
auto-
```

Examples:

```
auto-homeassistant.netfusiontechnologies.net
auto-homebridge.netfusiontechnologies.net
```

---

### Applications

User-facing or business applications.

Prefix:

```
app-
```

Examples:

```
app-odoo.netfusiontechnologies.net
app-ninja.netfusiontechnologies.net
app-unifi.netfusiontechnologies.net
```

---

## Access Layer (nginx / Edge)

Public/admin endpoints are separate from internal identity.

### Pattern

* Public/admin name → nginx (edge)
* Internal name → direct `.net`

Example:

```
vme3.netfusiontechnologies.xyz → nginx → nft-pve3
nft-pve3.netfusiontechnologies.net → 192.168.48.30
```

---

## DNS Rules

### Internal Identity

* All real systems MUST have a `.net` record
* Managed via Unbound host overrides

### Edge Routing

* `.xyz` and `.com` names resolve to nginx
* Implemented via Unbound aliases

### DHCP Naming

* `.home.arpa` managed by KEA
* Not used for infrastructure identity

---

## IP Addressing Guidance

### Same IP is acceptable when:

* Single service per container
* Multiple web apps behind nginx
* No special firewall or port requirements

### Separate IP required when:

* Non-HTTP ports required
* Different firewall policies needed
* Security isolation required
* Independent lifecycle desired

---

## Naming Guidelines

### Do

* Keep names short and descriptive
* Align hostname, FQDN, and Proxmox name
* Use prefixes to indicate role
* Keep `.net` as authoritative identity

### Do Not

* Use `.xyz` for internal identity
* Point `.net` names to nginx
* Mix multiple roles into one name
* Rely on DHCP for infrastructure DNS

---

## Examples (Complete Mapping)

```
Host:        nft-pve3.netfusiontechnologies.net
VM:          vm-bluestar.netfusiontechnologies.net
Database:    db-postgres.netfusiontechnologies.net
Service:     svc-grafana.netfusiontechnologies.net
Infra:       infra-nginx.netfusiontechnologies.net
Automation:  auto-homeassistant.netfusiontechnologies.net
Application: app-odoo.netfusiontechnologies.net

Public/Admin:
             grafana.netfusiontechnologies.xyz → nginx
             vme3.netfusiontechnologies.xyz → nginx
```

---

## Summary

This naming scheme provides:

* Clear separation of identity and access
* Predictable DNS behavior
* Scalable structure for future growth
* Consistency across infrastructure and services

---

## Future Enhancements

* Automate hostname enforcement via Ansible
* Standardize search domains per VLAN
* Introduce service discovery if needed
* Expand IPv6 naming and validation

---

End of document
