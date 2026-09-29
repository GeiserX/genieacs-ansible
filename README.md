<p align="center">
  <img src="https://raw.githubusercontent.com/GeiserX/genieacs-ansible/main/docs/images/banner.svg" alt="genieacs-ansible" width="900"/>
</p>

<h1 align="center">genieacs-ansible</h1>

<p align="center">
  <a href="https://github.com/GeiserX/genieacs-ansible/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/GeiserX/genieacs-ansible/ci.yml?branch=main&style=flat-square&logo=github&label=CI" alt="CI"/></a>
  <a href="https://github.com/GeiserX/genieacs-ansible/blob/main/LICENSE"><img src="https://img.shields.io/github/license/GeiserX/genieacs-ansible?style=flat-square" alt="License"/></a>
  <a href="https://galaxy.ansible.com/ui/repo/published/geiserx/genieacs/"><img src="https://img.shields.io/badge/galaxy-geiserx.genieacs-blue?style=flat-square&logo=ansible" alt="Ansible Galaxy"/></a>
  <a href="https://github.com/GeiserX/genieacs-ansible/stargazers"><img src="https://img.shields.io/github/stars/GeiserX/genieacs-ansible?style=flat-square&logo=github" alt="GitHub Stars"/></a>
</p>

<p align="center"><strong>Ansible Galaxy collection for managing GenieACS TR-069 ACS instances — dynamic inventory, device tasks, and configuration-as-code for presets and provisions.</strong></p>

## Features

- `geiserx.genieacs.genieacs` dynamic inventory: pulls CPE devices and groups them by manufacturer, model, firmware and tags.
- `geiserx.genieacs.genieacs_task`: create tasks on devices (reboot, firmware push, get/set parameters).
- `geiserx.genieacs.genieacs_preset`: create, read, update and delete presets (filter + provision mappings).
- `geiserx.genieacs.genieacs_provision`: create, read, update and delete provision scripts.
- Reads `ACS_URL`, `ACS_USER` and `ACS_PASS` from the environment.
- No third-party Python dependencies: HTTP goes through Ansible's own `open_url`.

## Quick start

```bash
ansible-galaxy collection install geiserx.genieacs
printf 'plugin: geiserx.genieacs.genieacs\nacs_url: http://genieacs:7557\n' > genieacs.yml
ansible-inventory -i genieacs.yml --graph
```

Requires Ansible >= 2.14. The inventory file name must end in `genieacs.yml` or `genieacs.yaml`. Install from source and the full option list: [Getting started](https://github.com/GeiserX/genieacs-ansible/blob/main/docs/getting-started.md).

## Documentation

- [Getting started](https://github.com/GeiserX/genieacs-ansible/blob/main/docs/getting-started.md): Galaxy, from source, requirements, first run
- [Configuration](https://github.com/GeiserX/genieacs-ansible/blob/main/docs/configuration.md): inventory file options, authentication, protecting the NBI API
- [Usage](https://github.com/GeiserX/genieacs-ansible/blob/main/docs/usage.md): dynamic inventory host variables and filtering, device tasks, presets and provisions as code

## Related projects

Part of the GenieACS family: [genieacs-container](https://github.com/GeiserX/genieacs-container), [genieacs-mcp](https://github.com/GeiserX/genieacs-mcp), [genieacs-ha](https://github.com/GeiserX/genieacs-ha), [genieacs-services](https://github.com/GeiserX/genieacs-services), [genieacs-sim-container](https://github.com/GeiserX/genieacs-sim-container). The full list is in [genieacs-container's related projects](https://github.com/GeiserX/genieacs-container/blob/main/docs/related.md).

## License

[GPL-3.0-or-later](https://github.com/GeiserX/genieacs-ansible/blob/main/LICENSE)
