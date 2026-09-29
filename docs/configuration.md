# Configuration

## Inventory file

The inventory file must end in `genieacs.yml` or `genieacs.yaml`. Its options:

| Option | Default | Description |
|--------|---------|-------------|
| `plugin` | | Always `geiserx.genieacs.genieacs` |
| `acs_url` | | GenieACS NBI URL, for example `http://genieacs:7557` (required; env `ACS_URL`) |
| `acs_username` | `""` | Basic-auth username (env `ACS_USER`) |
| `acs_password` | `""` | Basic-auth password (env `ACS_PASS`) |
| `device_query` | `""` | MongoDB-style JSON query to filter devices, for example `'{"_tags":"managed"}'` |
| `limit` | `0` | Maximum number of devices to fetch; `0` means no limit |
| `groups_from` | `[manufacturer, model, firmware, tags]` | Which groups to build |
| `timeout` | `30` | HTTP request timeout in seconds |

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
