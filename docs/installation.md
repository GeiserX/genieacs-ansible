# Installation

<p>
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python"/>
</p>

```bash
ansible-galaxy collection install geiserx.genieacs
```

Or from source:

```bash
git clone https://github.com/GeiserX/genieacs-ansible.git
cd genieacs-ansible
ansible-galaxy collection build
ansible-galaxy collection install geiserx-genieacs-*.tar.gz
```

Requires **Ansible >= 2.14** and **Python >= 3.10**. No external Python dependencies — uses only `urllib` from the standard library.
