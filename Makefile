SHELL := /bin/bash
ANSIBLE ?= ansible
PLAYBOOK ?= ansible-playbook
INVENTORY ?= inventories/production/hosts.yml
LIMIT ?=
PLAY ?=
CHECK ?=
DIFF ?= --diff

.PHONY: help inventory lint syntax check apply site sysalerts monitoring bootstrap hooks galaxy

help:
	@echo "Targets:"
	@echo "  make inventory"
	@echo "  make lint"
	@echo "  make syntax PLAY=playbooks/sysalerts.yml"
	@echo "  make check PLAY=playbooks/sysalerts.yml LIMIT=bluestar"
	@echo "  make apply PLAY=playbooks/sysalerts.yml LIMIT=bluestar"
	@echo "  make site"
	@echo "  make sysalerts LIMIT=host_or_group"
	@echo "  make monitoring LIMIT=host_or_group"
	@echo "  make bootstrap LIMIT=host_or_group"
	@echo "  make hooks"
	@echo "  make galaxy"

inventory:
	ansible-inventory --graph

lint:
	pre-commit run --all-files
	ansible-lint .

syntax:
	test -n "$(PLAY)"
	$(PLAYBOOK) $(PLAY) --syntax-check

check:
	test -n "$(PLAY)"
	$(PLAYBOOK) $(PLAY) $(if $(LIMIT),--limit $(LIMIT),) --check $(DIFF)

apply:
	test -n "$(PLAY)"
	$(PLAYBOOK) $(PLAY) $(if $(LIMIT),--limit $(LIMIT),)

site:
	$(PLAYBOOK) playbooks/site.yml $(if $(LIMIT),--limit $(LIMIT),)

sysalerts:
	$(PLAYBOOK) playbooks/sysalerts.yml $(if $(LIMIT),--limit $(LIMIT),)

monitoring:
	$(PLAYBOOK) playbooks/monitoring_prometheus.yml $(if $(LIMIT),--limit $(LIMIT),)

bootstrap:
	$(PLAYBOOK) playbooks/bootstrap_ansible_user_on_pvenodes.yml $(if $(LIMIT),--limit $(LIMIT),)

hooks:
	pre-commit install

galaxy:
	ansible-galaxy collection install -r requirements.yml
