# Usage

The collection ships one inventory plugin and three modules:

| Type | Plugin / Module | Description |
|------|----------------|-------------|
| **Inventory** | `geiserx.genieacs.genieacs` | Dynamic inventory that pulls CPE devices and groups them by manufacturer, model, firmware, and tags |
| **Module** | `geiserx.genieacs.genieacs_task` | Create tasks on devices (reboot, firmware push, get/set parameters) |
| **Module** | `geiserx.genieacs.genieacs_preset` | Create, read, update and delete presets (filter + provision mappings) |
| **Module** | `geiserx.genieacs.genieacs_provision` | Create, read, update and delete provision scripts |

## Dynamic inventory

Each host gets variables: `genieacs_id`, `genieacs_manufacturer`, `genieacs_model`, `genieacs_serial`, `genieacs_firmware`, `genieacs_hardware`, `genieacs_last_inform`, `genieacs_tags`, and `ansible_host` (set to the device IP).

### Filtering

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

All inventory options are on [Configuration](configuration.md#inventory-file).

## Device tasks

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

## Presets and provisions as code

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
