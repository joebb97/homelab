PRIVATE_BASE := $(HOME)/src/homelab-private
PRIVATE_VAULT := $(PRIVATE_BASE)/vault/vault.yml
VAULT := vault/vault.yml

.PHONY: setup link-vault

setup:
	git submodule update --init --recursive
	uv sync
	test -d $(PRIVATE_BASE) || git clone git@github.com:joebb97/homelab-private.git $(PRIVATE_BASE)
	$(MAKE) link-vault

link-vault:
	mkdir -p $(PRIVATE_BASE)/vault
	test -e $(PRIVATE_VAULT) || mv $(VAULT) $(PRIVATE_VAULT)
	ln -sf $(PRIVATE_VAULT) $(VAULT)

switches:
	uv run ansible-playbook -vvv configure-switches.yml --tags switches-real

switches-mock:
	uv run ansible-playbook -vvv configure-switches.yml --tags switches-mock
