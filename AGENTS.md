# Repository Instructions

- For Ansible tasks, use short module names such as `copy`, `template`, `file`, and `apt`; do not write fully qualified names like `ansible.builtin.copy`.
- Put reusable Ansible behavior in roles under `roles/` instead of adding large task blocks directly to playbooks.
