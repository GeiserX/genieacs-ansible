# Authentication and security

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
