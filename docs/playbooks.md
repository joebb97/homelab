# How to run playbooks

## Playbooks that require the ansible vault

You'll need to set ANSIBLE_VAULT_PASSWORD for playbooks that require the ansible vault. `scripts/vault-password-env` will print out this environment for ansible when it goes to decrypt the vault.

For me, I use passage to set the environment variable

`export ANSIBLE_VAULT_PASSWORD=$(passage path-to-vault-password)`

Then you can run the playbooks

`uv run ansible-playbook <playbook>`

example

`uv run ansible-playbook configure-vms.yml`

## Configure a host that doesn't have ssh keys on it yet

Assuming the ansible_user has sudo privile(-b connects and then becomes sudo). 

`uv run ansible-playbook configure-users.yml -e "ansible_password=$PW" --limit $HOST -b`

example `$HOST` is ryu.blueteam.lan

To run other ad-hoc commands on this host that doesn't have ssh keys yet

`uv run ansible other -e "ansible_password=$PW" -m command -a 'echo hi'`

## Run one part of a playbook

Use tags

`uv run ansible-playbook configure-vms.yml --tags syncthing`

## Check a playbook before running

`uv run ansible-playbook configure-samba.yml --check --diff`
