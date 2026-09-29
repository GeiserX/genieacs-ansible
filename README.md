<p align="center">
  <img src="https://raw.githubusercontent.com/GeiserX/genieacs-ansible/main/docs/images/banner.svg" alt="genieacs-ansible banner" width="900"/>
</p>

<h1 align="center">genieacs-ansible</h1>

<p align="center">
  <a href="https://galaxy.ansible.com/ui/repo/published/geiserx/genieacs/"><img src="https://img.shields.io/badge/galaxy-geiserx.genieacs-blue?style=flat-square&logo=ansible" alt="Ansible Galaxy"/></a>
  <a href="https://github.com/GeiserX/genieacs-ansible/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/GeiserX/genieacs-ansible/ci.yml?branch=main&style=flat-square&logo=github&label=CI" alt="CI"/></a>
  <a href="https://github.com/GeiserX/genieacs-ansible/stargazers"><img src="https://img.shields.io/github/stars/GeiserX/genieacs-ansible?style=flat-square&logo=github" alt="GitHub Stars"/></a>
  <a href="https://github.com/GeiserX/genieacs-ansible/blob/main/LICENSE"><img src="https://img.shields.io/github/license/GeiserX/genieacs-ansible?style=flat-square" alt="License"/></a>
</p>

<p align="center"><strong>Ansible Galaxy collection for managing GenieACS TR-069 ACS instances — dynamic inventory, device tasks, and configuration-as-code for presets and provisions.</strong></p>

## Features

- `geiserx.genieacs.genieacs` dynamic inventory: pulls CPE devices and groups them by manufacturer, model, firmware and tags.
- `geiserx.genieacs.genieacs_task`: create tasks on devices (reboot, firmware push, get/set parameters).
- `geiserx.genieacs.genieacs_preset`: create, read, update and delete presets (filter + provision mappings).
- `geiserx.genieacs.genieacs_provision`: create, read, update and delete provision scripts.
- Reads `ACS_URL`, `ACS_USER` and `ACS_PASS` from the environment.
- No external Python dependencies; it uses only `urllib` from the standard library.

## Quick start

```bash
ansible-galaxy collection install geiserx.genieacs
printf 'plugin: geiserx.genieacs.genieacs\nacs_url: http://genieacs:7557\n' > genieacs.yml
ansible-inventory -i genieacs.yml --graph
```

Requires Ansible >= 2.14 and Python >= 3.10. The inventory file name must end in `genieacs.yml` or `genieacs.yaml`.

## Documentation

- [Installation](https://github.com/GeiserX/genieacs-ansible/blob/main/docs/installation.md): Galaxy, from source, requirements
- [Dynamic inventory](https://github.com/GeiserX/genieacs-ansible/blob/main/docs/inventory.md): the inventory file, host variables, filtering
- [Modules](https://github.com/GeiserX/genieacs-ansible/blob/main/docs/modules.md): device tasks, presets and provisions as code
- [Authentication and security](https://github.com/GeiserX/genieacs-ansible/blob/main/docs/authentication.md): parameters, environment variables, protecting the NBI API

## Related projects

This collection is part of a broader set of tools for working with GenieACS:

| Project | Type | Description |
|---------|------|-------------|
| [genieacs-container](https://github.com/GeiserX/genieacs-container) | Docker + Helm | Production-ready multi-arch Docker image and Helm chart |
| [genieacs-mcp](https://github.com/GeiserX/genieacs-mcp) | MCP Server | AI-assisted device management via Model Context Protocol |
| [genieacs-ha](https://github.com/GeiserX/genieacs-ha) | HA Integration | Home Assistant integration for TR-069 monitoring |
| [n8n-nodes-genieacs](https://github.com/GeiserX/n8n-nodes-genieacs) | n8n Node | Workflow automation for GenieACS |
| [genieacs-services](https://github.com/GeiserX/genieacs-services) | Service Defs | Systemd/Supervisord service definitions |
| [genieacs-sim-container](https://github.com/GeiserX/genieacs-sim-container) | Simulator | Docker-based GenieACS simulator for testing |

## License

[GPL-3.0](https://github.com/GeiserX/genieacs-ansible/blob/main/LICENSE)
