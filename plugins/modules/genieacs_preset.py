#!/usr/bin/python
"""Ansible module to manage GenieACS presets."""

from __future__ import annotations

DOCUMENTATION = r"""
module: genieacs_preset
short_description: Manage GenieACS presets
description:
  - Create, update, or delete presets on a GenieACS instance via the NBI API.
  - Presets define a filter (precondition) and map to one or more provision scripts.
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
  name:
    description: Preset name (unique identifier in GenieACS).
    required: true
    type: str
  state:
    description: Whether the preset should exist or not.
    type: str
    choices: [present, absent]
    default: present
  precondition:
    description: >-
      MongoDB-style JSON filter string that determines which devices
      this preset applies to. Example: '{"_tags":"managed"}'
    type: str
    default: ""
  events:
    description: >-
      Dict mapping event names to booleans. Common events:
      0 BOOTSTRAP, 1 BOOT, 2 PERIODIC, 3 VALUE CHANGE, 4 CONNECTION REQUEST, etc.
    type: dict
    default: {}
  provisions:
    description: >-
      List of provisions to execute. Each item is a list where the first
      element is the provision name and remaining elements are arguments.
    type: list
    elements: list
    default: []
  weight:
    description: Preset priority weight (lower = higher priority).
    type: int
    default: 0
"""

EXAMPLES = r"""
- name: Create a preset for periodic inform
  geiserx.genieacs.genieacs_preset:
    acs_url: http://genieacs:7557
    name: inform_interval
    precondition: '{"_tags":"managed"}'
    events:
      "2 PERIODIC": true
    provisions:
      - ["set_inform_interval", "3600"]

- name: Delete a preset
  geiserx.genieacs.genieacs_preset:
    acs_url: http://genieacs:7557
    name: old_preset
    state: absent
"""

RETURN = r"""
preset:
  description: The preset object as stored in GenieACS (on present).
  type: dict
  returned: when state=present
"""

import json

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
            name=dict(type="str", required=True),
            state=dict(type="str", default="present", choices=["present", "absent"]),
            precondition=dict(type="str", default=""),
            events=dict(type="dict", default={}),
            provisions=dict(type="list", elements="list", default=[]),
            weight=dict(type="int", default=0),
        ),
        supports_check_mode=True,
    )

    client = GenieACSClient(
        module.params["acs_url"],
        module.params["acs_username"],
        module.params["acs_password"],
    )

    name = module.params["name"]
    state = module.params["state"]

    # Check current state
    try:
        existing = {p["_id"]: p for p in client.list_presets()}
    except GenieACSError as exc:
        module.fail_json(msg=str(exc))

    exists = name in existing

    if state == "absent":
        if not exists:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True)
        try:
            client.delete_preset(name)
        except GenieACSError as exc:
            module.fail_json(msg=str(exc))
        module.exit_json(changed=True)

    # state == present
    preset = {
        "precondition": module.params["precondition"],
        "events": module.params["events"],
        "configurations": [{"type": "provision", "name": p[0], "args": p[1:]} for p in module.params["provisions"]],
        "weight": module.params["weight"],
    }

    if exists:
        old = existing[name]
        # Compare relevant fields
        changed = (
            old.get("precondition", "") != preset["precondition"]
            or old.get("events", {}) != preset["events"]
            or old.get("configurations", []) != preset["configurations"]
            or old.get("weight", 0) != preset["weight"]
        )
        if not changed:
            module.exit_json(changed=False, preset=old)

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        client.put_preset(name, preset)
    except GenieACSError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, preset=preset)


if __name__ == "__main__":
    main()
