# Dynamic inventory

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

## Filtering

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
