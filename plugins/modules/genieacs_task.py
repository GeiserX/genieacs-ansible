#!/usr/bin/python
"""Ansible module to create tasks on GenieACS devices."""

from __future__ import annotations

DOCUMENTATION = r"""
module: genieacs_task
short_description: Create a task on a GenieACS CPE device
description:
  - Enqueue a task (reboot, firmware download, get/set parameter values)
    on a device managed by GenieACS via the NBI API.
version_added: "0.1.0"
author:
  - Sergio Fernandez (@GeiserX)
options:
  acs_url:
    description: GenieACS NBI API URL.
    required: true
    type: str
  acs_username:
    description: Basic-auth username.
    type: str
    default: ""
  acs_password:
    description: Basic-auth password.
    type: str
    default: ""
    no_log: true
  device_id:
    description: The GenieACS device ID.
    required: true
    type: str
  task_name:
    description: >-
      Task type. One of: reboot, download, getParameterValues,
      setParameterValues, addObject, deleteObject, refreshObject.
    required: true
    type: str
    choices:
      - reboot
      - download
      - getParameterValues
      - setParameterValues
      - addObject
      - deleteObject
      - refreshObject
  parameter_names:
    description: >-
      List of parameter paths for getParameterValues / refreshObject.
    type: list
    elements: str
    default: []
  parameter_values:
    description: >-
      List of [path, value, type] triples for setParameterValues.
      Example: [["InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID", "MySSID", "xsd:string"]]
    type: list
    elements: list
    default: []
  file_id:
    description: File ID (from GridFS) for download tasks.
    type: str
    default: ""
  timeout_ms:
    description: Connection request timeout in milliseconds.
    type: int
    default: 3000
"""

EXAMPLES = r"""
- name: Reboot a CPE device
  geiserx.genieacs.genieacs_task:
    acs_url: http://genieacs:7557
    device_id: "001122-Device-AABBCC"
    task_name: reboot

- name: Set WiFi SSID
  geiserx.genieacs.genieacs_task:
    acs_url: http://genieacs:7557
    device_id: "001122-Device-AABBCC"
    task_name: setParameterValues
    parameter_values:
      - ["InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID", "NewSSID", "xsd:string"]

- name: Push firmware
  geiserx.genieacs.genieacs_task:
    acs_url: http://genieacs:7557
    device_id: "001122-Device-AABBCC"
    task_name: download
    file_id: "firmware-v2.0.bin"
"""

RETURN = r"""
task:
  description: The created task object returned by GenieACS.
  type: dict
  returned: success
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.geiserx.genieacs.plugins.module_utils.genieacs_client import (
        GenieACSClient,
        GenieACSError,
    )
except ImportError:
    from ..module_utils.genieacs_client import GenieACSClient, GenieACSError


def main():
    module = AnsibleModule(
        argument_spec=dict(
            acs_url=dict(type="str", required=True),
            acs_username=dict(type="str", default=""),
            acs_password=dict(type="str", default="", no_log=True),
            device_id=dict(type="str", required=True),
            task_name=dict(
                type="str", required=True,
                choices=["reboot", "download", "getParameterValues",
                         "setParameterValues", "addObject", "deleteObject", "refreshObject"],
            ),
            parameter_names=dict(type="list", elements="str", default=[]),
            parameter_values=dict(type="list", elements="list", default=[]),
            file_id=dict(type="str", default=""),
            timeout_ms=dict(type="int", default=3000),
        ),
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=True, msg="Task would be created (check mode)")

    client = GenieACSClient(
        module.params["acs_url"],
        module.params["acs_username"],
        module.params["acs_password"],
    )

    task_body: dict = {"name": module.params["task_name"]}

    name = module.params["task_name"]
    if name in ("getParameterValues", "refreshObject"):
        task_body["parameterNames"] = module.params["parameter_names"]
    elif name == "setParameterValues":
        task_body["parameterValues"] = module.params["parameter_values"]
    elif name == "download":
        task_body["file"] = module.params["file_id"]

    try:
        result = client.create_task(
            module.params["device_id"],
            task_body,
            timeout_ms=module.params["timeout_ms"],
        )
    except GenieACSError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, task=result)


if __name__ == "__main__":
    main()
