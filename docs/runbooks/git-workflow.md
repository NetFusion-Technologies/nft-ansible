# NetFusion Ansible Runbook & Architecture

---

# Git Workflow

## Overview

This repository uses a hybrid structure:

- Main repo (nft-ansible)
  - inventories
  - playbooks
  - scripts
  - site-specific configuration
  - routeros collection (in-tree)

- Submodules
  - sysalerts
  - monitoring

This allows reusable collections to be versioned independently while keeping deployment logic centralized.

---

## Repository Layout

    nft-ansible/
    ├── inventories/
    ├── playbooks/
    ├── scripts/
    ├── collections/
    │   └── ansible_collections/
    │       └── netfusion/
    │           ├── sysalerts/   (submodule)
    │           ├── monitoring/  (submodule)
    │           └── routeros/    (in-tree)

---

## Key Concepts

### Main Repo vs Submodules

| Area | Where to commit |
|------|----------------|
| inventories | main repo |
| playbooks | main repo |
| routeros | main repo |
| sysalerts roles | submodule |
| monitoring roles | submodule |

---

## Start of Day

    cd ~/.ansible/projects/nft-ansible
    git pull
    git submodule update --init --recursive

---

## Working in Main Repo

Used for:
- playbooks
- inventory
- routeros
- vars
- scripts

    git status
    git add <files>
    git commit -m "Describe change"
    git push

---

## Working in a Submodule (sysalerts / monitoring)

Step 1 — Enter submodule

    cd collections/ansible_collections/netfusion/sysalerts

Step 2 — Commit inside submodule

    git status
    git add .
    git commit -m "Describe change"
    git push

Step 3 — Update pointer in main repo

    cd ~/.ansible/projects/nft-ansible
    git add collections/ansible_collections/netfusion/sysalerts
    git commit -m "Update sysalerts submodule pointer"
    git push

---

## Important Rule

Submodule changes require TWO commits:

1. Commit inside submodule repo  
2. Commit updated pointer in main repo  

---

## Mixed Changes

    # Submodule
    cd collections/.../sysalerts
    git add .
    git commit -m "Add feature"
    git push

    # Main repo
    cd ~/.ansible/projects/nft-ansible
    git add playbooks collections/.../sysalerts
    git commit -m "Use updated sysalerts"
    git push

---

## Checking Status

    git status
    git submodule status

---

## Cloning Repo

    git clone --recurse-submodules https://github.com/NetFusion-Technologies/nft-ansible.git

---

## Pulling Updates

    git pull
    git submodule update --init --recursive

---

## DO NOT DO

    git submodule update --remote

---

## Pre-Run Checks

    git status
    git submodule status
    ansible-inventory --graph

---

## Running Playbooks Safely

    ansible-playbook playbooks/<file>.yml --check --diff

---

## Common Pitfalls

Forgot submodule pointer commit:

    git add collections/.../sysalerts
    git commit -m "Update submodule"

Edited submodule but didn’t push:

    cd submodule
    git push

---

## RouterOS Development

    git add collections/.../routeros
    git commit -m "Update routeros role"
    git push

---

## Golden Rules

1. Submodules require two commits  
2. Main repo controls deployment  
3. Always update submodules after pull  
4. Keep commits small and logical  
5. Never assume submodules auto-update  

---

# Architecture

## Overview

This repository implements an enterprise-grade Ansible architecture designed for:

- multi-environment deployments
- multi-customer reuse
- modular automation via collections

---

## Core Design Principles

1. Separation of concerns  
2. Reusable collections  
3. Environment-specific orchestration  
4. Version-controlled infrastructure  
5. Secure secret handling  

---

## Architecture Layers

### Site Repository (nft-ansible)

Responsible for:

- inventories  
- playbooks  
- environment-specific variables  
- orchestration logic  

Defines how infrastructure is deployed.

---

### Collections (Reusable Logic)

Collections contain:

- roles  
- modules  
- templates  
- defaults  

Current collections:

    netfusion.sysalerts
    netfusion.monitoring
    netfusion.routeros (in development)

Defines what gets deployed.

---

### Submodules

Collections are included as Git submodules:

    collections/ansible_collections/netfusion/

Benefits:

- independent versioning  
- reuse across environments  
- clean separation of logic  

---

## Deployment Model

    [ Site Repo ]
        ↓
    [ Playbooks ]
        ↓
    [ Collections ]
        ↓
    [ Infrastructure ]

---

## Inventory Structure

    inventories/
    └── production/
        ├── hosts.yml
        ├── group_vars/
        └── host_vars/

---

## Collection Responsibilities

### sysalerts

- postfix relay configuration  
- alert routing  
- email normalization  

---

### monitoring

- Prometheus  
- Alertmanager  
- Grafana  
- exporters  

---

### routeros

- MikroTik automation  
- MKTXP exporter  
- network provisioning  

---

## Security Model

Secrets:
- stored in Ansible Vault  
- never committed in plaintext  
- environment-specific vault files  

Sensitive data:
- stored under archive/  
- permissions set to 0600  
- secrets filtered  

---

## Execution Flow

1. Operator runs playbook  
2. Inventory defines targets  
3. Playbook calls roles  
4. Roles execute from collections  
5. Infrastructure converges  

---

## Multi-Environment Strategy

    production/
    staging/
    lab/

Each environment has:
- separate inventory  
- separate vault  
- shared collections  

---

## Versioning Strategy

- main repo tracks deployment state  
- submodules pin collection versions  
- updates are explicit and controlled  

---

## Future Expansion

- CI/CD (GitHub Actions)  
- ansible-lint enforcement  
- automated testing  
- Galaxy publishing  
- multi-tenant deployments  

---

## Summary

| Component | Purpose |
|----------|--------|
| nft-ansible | orchestration |
| sysalerts | alerting |
| monitoring | observability |
| routeros | network automation |

---

## Design Outcome

This architecture enables:

- repeatable deployments  
- reusable automation  
- scalable infrastructure  
- enterprise-grade maintainability  
