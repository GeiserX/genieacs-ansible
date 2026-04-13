<p align="center">
  <img src="docs/images/banner.svg" alt="genieacs-ansible banner" width="900"/>
</p>

<h1 align="center">genieacs-ansible</h1>

<p align="center">
  <a href="https://galaxy.ansible.com/ui/repo/published/geiserx/genieacs/"><img src="https://img.shields.io/badge/galaxy-geiserx.genieacs-blue?style=flat-square&logo=ansible" alt="Ansible Galaxy"/></a>
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <a href="https://github.com/GeiserX/genieacs-ansible/stargazers"><img src="https://img.shields.io/github/stars/GeiserX/genieacs-ansible?style=flat-square&logo=github" alt="GitHub Stars"/></a>
  <a href="https://github.com/GeiserX/genieacs-ansible/blob/main/LICENSE"><img src="https://img.shields.io/github/license/GeiserX/genieacs-ansible?style=flat-square" alt="License"/></a>
</p>

<p align="center"><strong>Ansible Galaxy collection for managing GenieACS TR-069 ACS instances — dynamic inventory, device tasks, and configuration-as-code for presets and provisions.</strong></p>

---

## Features

| Type | Plugin / Module | Description |
|------|----------------|-------------|
| **Inventory** | `geiserx.genieacs.genieacs` | Dynamic inventory that pulls CPE devices and groups them by manufacturer, model, firmware, and tags |
| **Module** | `geiserx.genieacs.genieacs_task` | Create tasks on devices (reboot, firmware push, get/set parameters) |
| **Module** | `geiserx.genieacs.genieacs_preset` | CRUD for presets (filter + provision mappings) |
| **Module** | `geiserx.genieacs.genieacs_provision` | CRUD for provision scripts |

## Installation

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

## Quick Start

### Dynamic Inventory

Create an inventory file ending in `genieacs.yml` or `genieacs.yaml` (this suffix is required for the plugin to recognize the file):

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

Each host gets variables: `genieacs_id`, `genieacs_manufacturer`, `genieacs_model`, `genieacs_serial`, `genieacs_firmware`, `genieacs_hardware`, `genieacs_last_inform`, `genieacs_tags`, and `ansible_host` (set to the device IP).

#### Filtering

Only include devices with a specific tag:

```yaml
plugin: geiserx.genieacs.genieacs
acs_url: http://genieacs:7557
device_query: '{"_tags":"managed"}'
limit: 500
groups_from:
  - manufacturer
  - model
  - tags
```

### Device Tasks

```yaml
- hosts: tag_managed
  tasks:
    - name: Reboot all managed devices
      geiserx.genieacs.genieacs_task:
        acs_url: http://genieacs:7557
        device_id: "{{ genieacs_id }}"
        task_name: reboot

    - name: Set WiFi SSID fleet-wide
      geiserx.genieacs.genieacs_task:
        acs_url: http://genieacs:7557
        device_id: "{{ genieacs_id }}"
        task_name: setParameterValues
        parameter_values:
          - ["InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID", "CompanyWiFi", "xsd:string"]

    - name: Push firmware to TP-Link devices
      geiserx.genieacs.genieacs_task:
        acs_url: http://genieacs:7557
        device_id: "{{ genieacs_id }}"
        task_name: download
        file_id: "firmware-v2.0.bin"
      when: genieacs_manufacturer == "TP-Link"
```

### Presets as Code

```yaml
- hosts: localhost
  tasks:
    - name: Deploy inform interval preset
      geiserx.genieacs.genieacs_preset:
        acs_url: http://genieacs:7557
        name: inform_interval
        precondition: '{"_tags":"managed"}'
        events:
          "2 PERIODIC": true
        provisions:
          - ["set_inform_interval", "3600"]

    - name: Upload provision script
      geiserx.genieacs.genieacs_provision:
        acs_url: http://genieacs:7557
        name: set_inform_interval
        script: |
          const now = Date.now();
          declare("InternetGatewayDevice.ManagementServer.PeriodicInformInterval",
                  {value: now}, {value: [args[0] || "3600", "xsd:unsignedInt"]});
```

## Authentication

The inventory plugin reads `ACS_URL`, `ACS_USER`, and `ACS_PASS` from environment variables automatically. Modules also support env vars via `fallback=(env_fallback, ...)`:

| Parameter | Environment Variable | Description |
|-----------|---------------------|-------------|
| `acs_url` | `ACS_URL` | GenieACS NBI URL (required) |
| `acs_username` | `ACS_USER` | Basic-auth username |
| `acs_password` | `ACS_PASS` | Basic-auth password |

> **Do not embed credentials in `acs_url`** (e.g. `http://user:pass@host:7557`). The URL is not masked in Ansible output. Always use the separate `acs_username` / `acs_password` parameters or their environment variables.

## Security

The GenieACS NBI API (port 7557) provides unauthenticated fleet-wide control by default — device reboots, firmware pushes, parameter changes, and more. **Do not expose it to untrusted networks.** Recommendations:

- Run NBI on a dedicated management VLAN or behind a reverse proxy with TLS and authentication.
- Use GenieACS's built-in NBI authentication (`NBI_ONLY` config) or a reverse proxy (Caddy, nginx) for TLS termination.
- Restrict access via firewall rules to only the hosts that need it (your Ansible controller, monitoring, etc.).

## GenieACS Ecosystem

This collection is part of a broader set of tools for working with GenieACS:

| Project | Type | Description |
|---------|------|-------------|
| [genieacs-container](https://github.com/GeiserX/genieacs-container) | Docker + Helm | Production-ready multi-arch Docker image and Helm chart |
| [genieacs-mcp](https://github.com/GeiserX/genieacs-mcp) | MCP Server | AI-assisted device management via Model Context Protocol |
| [genieacs-ha](https://github.com/GeiserX/genieacs-ha) | HA Integration | Home Assistant integration for TR-069 monitoring |
| [n8n-nodes-genieacs](https://github.com/GeiserX/n8n-nodes-genieacs) | n8n Node | Workflow automation for GenieACS |
| [genieacs-services](https://github.com/GeiserX/genieacs-services) | Service Defs | Systemd/Supervisord service definitions |
| [genieacs-sim-container](https://github.com/GeiserX/genieacs-sim-container) | Simulator | Docker-based GenieACS simulator for testing |


## Related Projects

| Project | Description |
|---------|-------------|
| [genieacs-container](https://github.com/GeiserX/genieacs-container) | Original and most popular Helm Chart / Container for GenieACS |
| [genieacs-sim-container](https://github.com/GeiserX/genieacs-sim-container) | Docker for the GenieACS Simulator |
| [genieacs-ha](https://github.com/GeiserX/genieacs-ha) | Home Assistant custom integration for GenieACS TR-069 router management |
| [genieacs-mcp](https://github.com/GeiserX/genieacs-mcp) | MCP Server for GenieACS written in Go |
| [genieacs-services](https://github.com/GeiserX/genieacs-services) | Systemd/Supervisord services for GenieACS processes |
| [n8n-nodes-genieacs](https://github.com/GeiserX/n8n-nodes-genieacs) | n8n community node for GenieACS TR-069 device management |

## License

[GPL-3.0](LICENSE)
