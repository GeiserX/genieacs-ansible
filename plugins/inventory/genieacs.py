# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Sergio Fernandez (@GeiserX)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
"""Dynamic inventory plugin for GenieACS.

Pulls devices from a GenieACS NBI endpoint and groups them
by manufacturer, model, firmware version, and tags.

Example inventory file (genieacs.yml):
    plugin: geiserx.genieacs.genieacs
    acs_url: http://genieacs:7557
    # acs_username: admin
    # acs_password: admin
    # device_query: '{"_tags":"managed"}'
    # limit: 500
    # groups_from:
    #   - manufacturer
    #   - model
    #   - firmware
    #   - tags
"""

from __future__ import annotations

DOCUMENTATION = r"""
name: genieacs
short_description: GenieACS dynamic inventory plugin
description:
  - Pulls CPE devices from a GenieACS NBI API and creates inventory hosts
    grouped by manufacturer, model, firmware version, and tags.
author:
  - Sergio Fernandez (@GeiserX)
version_added: "0.1.0"
options:
  acs_url:
    description: GenieACS NBI API URL (e.g. http://genieacs:7557).
    required: true
    type: str
    env:
      - name: ACS_URL
  acs_username:
    description: Basic-auth username for the NBI API.
    type: str
    default: ""
    env:
      - name: ACS_USER
  acs_password:
    description: Basic-auth password for the NBI API.
    type: str
    default: ""
    env:
      - name: ACS_PASS
  device_query:
    description: >-
      MongoDB-style JSON query to filter devices.
      Example: '{"_tags":"managed"}' to only include tagged devices.
    type: str
    default: ""
  limit:
    description: Maximum number of devices to fetch (0 = unlimited).
    type: int
    default: 0
  groups_from:
    description: >-
      List of grouping strategies. Supported values -
      manufacturer, model, firmware, tags.
    type: list
    elements: str
    default:
      - manufacturer
      - model
      - firmware
      - tags
  timeout:
    description: HTTP request timeout in seconds.
    type: int
    default: 30
"""

EXAMPLES = r"""
# Minimal — fetch all devices
plugin: geiserx.genieacs.genieacs
acs_url: http://genieacs:7557

# With auth and filtering
plugin: geiserx.genieacs.genieacs
acs_url: http://genieacs:7557
acs_username: admin
acs_password: secret
device_query: '{"_tags":"managed"}'
limit: 1000
groups_from:
  - manufacturer
  - model
  - tags
"""

import re

from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display

display = Display()

try:
    from ansible_collections.geiserx.genieacs.plugins.module_utils.genieacs_client import (
        GenieACSClient,
        GenieACSError,
    )
except ImportError:
    from ..module_utils.genieacs_client import GenieACSClient, GenieACSError


def _safe_group(name: str) -> str:
    """Sanitize a string into a valid Ansible group name."""
    return re.sub(r"[^A-Za-z0-9_]", "_", str(name)).strip("_").lower()


def _deep_get(obj: dict, *keys: str, default=""):
    """Walk nested dicts/lists to extract a TR-069 parameter value."""
    cur = obj
    for k in keys:
        if isinstance(cur, dict):
            cur = cur.get(k, {})
        else:
            return default
    if isinstance(cur, dict):
        return cur.get("_value", cur.get("value", default))
    return cur if cur else default


class InventoryModule(BaseInventoryPlugin):
    NAME = "geiserx.genieacs.genieacs"

    def verify_file(self, path: str) -> bool:
        if super().verify_file(path):
            return path.endswith(("genieacs.yml", "genieacs.yaml"))
        return False

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path, cache)
        self._read_config_data(path)

        acs_url = self.get_option("acs_url")
        username = self.get_option("acs_username")
        password = self.get_option("acs_password")
        device_query = self.get_option("device_query")
        limit = self.get_option("limit")
        groups_from = self.get_option("groups_from")
        timeout = self.get_option("timeout")

        client = GenieACSClient(acs_url, username, password, timeout=timeout)

        try:
            devices = client.list_devices(query=device_query, limit=limit)
        except GenieACSError as exc:
            raise AnsibleParserError(f"Failed to fetch devices from GenieACS: {exc}") from exc

        self.inventory.add_group("genieacs")
        seen_hostnames: dict[str, str] = {}

        for dev in devices:
            device_id = dev.get("_id", "")
            if not device_id:
                continue

            hostname = _safe_group(device_id)
            if hostname in seen_hostnames:
                display.warning(
                    f"GenieACS device ID '{device_id}' sanitizes to hostname '{hostname}' "
                    f"which collides with device '{seen_hostnames[hostname]}'. "
                    f"Host vars will be overwritten."
                )
            seen_hostnames[hostname] = device_id
            self.inventory.add_host(hostname, group="genieacs")

            # Extract common TR-069 summary fields
            manufacturer = _deep_get(dev, "summary", "manufacturer")
            model = _deep_get(dev, "summary", "productClass") or _deep_get(dev, "summary", "modelName")
            serial = _deep_get(dev, "summary", "serialNumber")
            firmware = _deep_get(dev, "summary", "softwareVersion")
            hardware = _deep_get(dev, "summary", "hardwareVersion")
            last_inform = _deep_get(dev, "summary", "lastInform")
            ip = _deep_get(dev, "summary", "ip")
            tags = dev.get("_tags", [])

            # Set host variables
            self.inventory.set_variable(hostname, "genieacs_id", device_id)
            self.inventory.set_variable(hostname, "genieacs_manufacturer", manufacturer)
            self.inventory.set_variable(hostname, "genieacs_model", model)
            self.inventory.set_variable(hostname, "genieacs_serial", serial)
            self.inventory.set_variable(hostname, "genieacs_firmware", firmware)
            self.inventory.set_variable(hostname, "genieacs_hardware", hardware)
            self.inventory.set_variable(hostname, "genieacs_last_inform", last_inform)
            self.inventory.set_variable(hostname, "genieacs_tags", tags)
            if ip:
                self.inventory.set_variable(hostname, "ansible_host", ip)

            # Dynamic grouping
            if "manufacturer" in groups_from and manufacturer:
                grp = f"manufacturer_{_safe_group(manufacturer)}"
                self.inventory.add_group(grp)
                self.inventory.add_child(grp, hostname)

            if "model" in groups_from and model:
                grp = f"model_{_safe_group(model)}"
                self.inventory.add_group(grp)
                self.inventory.add_child(grp, hostname)

            if "firmware" in groups_from and firmware:
                grp = f"firmware_{_safe_group(firmware)}"
                self.inventory.add_group(grp)
                self.inventory.add_child(grp, hostname)

            if "tags" in groups_from and tags:
                for tag in tags:
                    grp = f"tag_{_safe_group(tag)}"
                    self.inventory.add_group(grp)
                    self.inventory.add_child(grp, hostname)
