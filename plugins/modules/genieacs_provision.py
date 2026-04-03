#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Sergio Fernandez (@GeiserX)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
"""Ansible module to manage GenieACS provision scripts."""

from __future__ import annotations

DOCUMENTATION = r"""
module: genieacs_provision
short_description: Manage GenieACS provision scripts
description:
  - Create, update, or delete provision scripts on a GenieACS instance.
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
  name:
    description: Provision script name.
    required: true
    type: str
  state:
    description: Whether the provision should exist or not.
    type: str
    choices: [present, absent]
    default: present
  script:
    description: JavaScript provision script content.
    type: str
    default: ""
  script_file:
    description: Path to a file containing the provision script.
    type: path
    default: ""
"""

EXAMPLES = r"""
- name: Upload a provision script
  geiserx.genieacs.genieacs_provision:
    acs_url: http://genieacs:7557
    name: set_inform_interval
    script: |
      const now = Date.now();
      declare("InternetGatewayDevice.ManagementServer.PeriodicInformInterval",
              {value: now}, {value: [args[0] || "3600", "xsd:unsignedInt"]});

- name: Upload from file
  geiserx.genieacs.genieacs_provision:
    acs_url: http://genieacs:7557
    name: my_provision
    script_file: provisions/my_provision.js
"""

RETURN = r"""
name:
  description: The provision name.
  type: str
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule, env_fallback

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
            acs_url=dict(type="str", required=True, fallback=(env_fallback, ["ACS_URL"])),
            acs_username=dict(type="str", default="", fallback=(env_fallback, ["ACS_USER"])),
            acs_password=dict(type="str", default="", no_log=True, fallback=(env_fallback, ["ACS_PASS"])),
            name=dict(type="str", required=True),
            state=dict(type="str", default="present", choices=["present", "absent"]),
            script=dict(type="str", default=""),
            script_file=dict(type="path", default=""),
        ),
        mutually_exclusive=[("script", "script_file")],
        supports_check_mode=True,
    )

    client = GenieACSClient(
        module.params["acs_url"],
        module.params["acs_username"],
        module.params["acs_password"],
    )

    name = module.params["name"]
    state = module.params["state"]

    try:
        existing = {p["_id"]: p.get("script", "") for p in client.list_provisions()}
    except GenieACSError as exc:
        module.fail_json(msg=str(exc))

    exists = name in existing

    if state == "absent":
        if not exists:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True)
        try:
            client.delete_provision(name)
        except GenieACSError as exc:
            module.fail_json(msg=str(exc))
        module.exit_json(changed=True, name=name)

    # state == present
    script = module.params["script"]
    if module.params["script_file"]:
        with open(module.params["script_file"]) as fh:
            script = fh.read()

    if not script:
        module.fail_json(msg="Either 'script' or 'script_file' is required when state=present")

    if exists and existing[name] == script:
        module.exit_json(changed=False, name=name)

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        client.put_provision(name, script)
    except GenieACSError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, name=name)


if __name__ == "__main__":
    main()
