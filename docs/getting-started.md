# Getting started

## Install

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

Requires **Ansible >= 2.14** (`meta/runtime.yml`); CI tests on Python 3.12. No third-party Python
dependencies: HTTP goes through Ansible's own `open_url`.

## First run

Create an inventory file ending in `genieacs.yml` or `genieacs.yaml` (the plugin only picks up files
with that suffix):

```yaml
plugin: geiserx.genieacs.genieacs
acs_url: http://genieacs:7557
# acs_username: admin
# acs_password: admin
```

Test it:

```bash
ansible-inventory -i genieacs.yml --graph
```

Output:

```
@all:
  |--@genieacs:
  |  |--001122_device_aabbcc
  |  |--334455_device_ddeeff
  |--@manufacturer_tp_link:
  |  |--001122_device_aabbcc
  |--@model_archer_vr600:
  |  |--001122_device_aabbcc
  |--@firmware_0_9_1_3_3:
  |  |--001122_device_aabbcc
  |--@tag_managed:
  |  |--001122_device_aabbcc
  |  |--334455_device_ddeeff
```

Each device is a host, grouped by manufacturer, model, firmware and tags. Every option of the file is on
[Configuration](configuration.md); the modules are on [Usage](usage.md).
