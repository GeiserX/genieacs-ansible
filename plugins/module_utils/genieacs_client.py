"""Thin wrapper around the GenieACS NBI REST API."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urljoin
from urllib.request import Request, urlopen

__all__ = ["GenieACSClient", "GenieACSError"]


class GenieACSError(Exception):
    pass


class GenieACSClient:
    """Minimal HTTP client for the GenieACS NBI (port 7557)."""

    def __init__(self, base_url: str, username: str = "", password: str = "", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._auth_header = None
        if username:
            import base64
            cred = base64.b64encode(f"{username}:{password}".encode()).decode()
            self._auth_header = f"Basic {cred}"

    def _request(self, method: str, path: str, query: dict | None = None,
                 data: bytes | None = None, content_type: str = "application/json") -> bytes:
        url = f"{self.base_url}{path}"
        if query:
            url += "?" + urlencode(query)
        req = Request(url, data=data, method=method)
        req.add_header("Content-Type", content_type)
        if self._auth_header:
            req.add_header("Authorization", self._auth_header)
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                return resp.read()
        except HTTPError as exc:
            body = exc.read().decode(errors="replace")
            raise GenieACSError(f"HTTP {exc.code} on {method} {path}: {body}") from exc
        except URLError as exc:
            raise GenieACSError(f"Connection failed: {exc.reason}") from exc

    def _get_json(self, path: str, query: dict | None = None) -> list | dict:
        raw = self._request("GET", path, query=query)
        return json.loads(raw) if raw else []

    # ── Devices ─────────────────────────────────────────────
    def list_devices(self, query: str = "", projection: str = "", limit: int = 0) -> list[dict]:
        params: dict[str, str] = {}
        if query:
            params["query"] = query
        if projection:
            params["projection"] = projection
        if limit > 0:
            params["limit"] = str(limit)
        return self._get_json("/devices", params)

    def get_device(self, device_id: str) -> dict | None:
        devices = self.list_devices(query=json.dumps({"_id": device_id}))
        return devices[0] if devices else None

    def delete_device(self, device_id: str) -> None:
        self._request("DELETE", f"/devices/{quote(device_id, safe='')}")

    # ── Tasks ───────────────────────────────────────────────
    def create_task(self, device_id: str, task: dict, timeout_ms: int = 3000) -> dict:
        path = f"/devices/{quote(device_id, safe='')}/tasks"
        params = {"timeout": str(timeout_ms), "connection_request": ""}
        raw = self._request("POST", path, query=params, data=json.dumps(task).encode())
        return json.loads(raw) if raw else {}

    # ── Presets ─────────────────────────────────────────────
    def list_presets(self) -> list[dict]:
        return self._get_json("/presets")

    def put_preset(self, name: str, preset: dict) -> None:
        self._request("PUT", f"/presets/{quote(name, safe='')}", data=json.dumps(preset).encode())

    def delete_preset(self, name: str) -> None:
        self._request("DELETE", f"/presets/{quote(name, safe='')}")

    # ── Provisions ──────────────────────────────────────────
    def list_provisions(self) -> list[dict]:
        return self._get_json("/provisions")

    def put_provision(self, name: str, script: str) -> None:
        self._request("PUT", f"/provisions/{quote(name, safe='')}", data=script.encode(),
                       content_type="text/plain")

    def delete_provision(self, name: str) -> None:
        self._request("DELETE", f"/provisions/{quote(name, safe='')}")

    # ── Virtual Parameters ──────────────────────────────────
    def list_virtual_parameters(self) -> list[dict]:
        return self._get_json("/virtual_parameters")

    def put_virtual_parameter(self, name: str, script: str) -> None:
        self._request("PUT", f"/virtual_parameters/{quote(name, safe='')}", data=script.encode(),
                       content_type="text/plain")

    def delete_virtual_parameter(self, name: str) -> None:
        self._request("DELETE", f"/virtual_parameters/{quote(name, safe='')}")

    # ── Files ───────────────────────────────────────────────
    def list_files(self) -> list[dict]:
        return self._get_json("/files")

    def put_file(self, filename: str, data: bytes, file_type: str = "1 Firmware Upgrade Image",
                 oui: str = "", product_class: str = "", version: str = "") -> None:
        path = f"/files/{quote(filename, safe='')}"
        headers_qs: dict[str, str] = {"fileType": file_type}
        if oui:
            headers_qs["oui"] = oui
        if product_class:
            headers_qs["productClass"] = product_class
        if version:
            headers_qs["version"] = version
        self._request("PUT", path, query=headers_qs, data=data,
                       content_type="application/octet-stream")

    def delete_file(self, filename: str) -> None:
        self._request("DELETE", f"/files/{quote(filename, safe='')}")

    # ── Config ──────────────────────────────────────────────
    def get_config(self) -> dict:
        return self._get_json("/config")

    def put_config(self, key: str, value: str) -> None:
        self._request("PUT", f"/config/{quote(key, safe='')}", data=json.dumps(value).encode())

    def delete_config(self, key: str) -> None:
        self._request("DELETE", f"/config/{quote(key, safe='')}")

    # ── Faults ──────────────────────────────────────────────
    def list_faults(self, query: str = "") -> list[dict]:
        params = {"query": query} if query else {}
        return self._get_json("/faults", params)

    def delete_fault(self, fault_id: str) -> None:
        self._request("DELETE", f"/faults/{quote(fault_id, safe='')}")
