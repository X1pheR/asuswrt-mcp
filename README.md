# ASUSWRT MCP

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

mcp-name: io.github.x1pher/asuswrt-mcp

A community-maintained **independent downstream** of [teefloo/asuswrt-mcp](https://github.com/teefloo/asuswrt-mcp) for secure, controlled administration of AsusWRT and AsusWRT-Merlin routers over SSH. It is maintained as its own product and release line, while retaining clear upstream provenance. It is not affiliated with or endorsed by ASUS or the upstream project.

## Why this downstream exists

The upstream baseline already provides a strong allowlisted SSH-based MCP surface. This independent downstream exists because broader day-to-day router observability and several ASUS-specific correctness fixes were needed **without** adding arbitrary SSH/NVRAM access or exposing sensitive router data. It follows its own roadmap, release verification, package identity, and safety boundary rather than using upstream as the active release line.

Compared with the pinned upstream baseline, the current candidate expands the surface from **47 to 67 tools** while keeping mutations guarded:

- **19 additional read tools** for firewall posture, per-radio Wi-Fi configuration and scheduling, DNS Filter/Privacy, QoS, AiProtection, AiMesh, VLAN/guest segmentation, Dual-WAN, WPS, Smart Connect/roaming, firmware-update status, VPN-client health, WAN watchdog, logging, traffic-monitoring posture and auxiliary-service posture.
- **Bounded WireGuard client management** for connect, disconnect and restart of already-configured client slots only; profile creation/import/edit and credential exposure remain excluded.
- **Correctness fixes** for ASUS SSH enable-state semantics, WireGuard-client detection and bulk NVRAM reads where empty values could otherwise corrupt the following key/value record.
- **Data minimization** for sensitive families: status/count metadata is preferred over resolver values, VPN peer/endpoint data, client policy bodies, credentials or raw rule payloads.

Generic correctness fixes can be proposed upstream independently. This maintained downstream owns the broader opinionated capability and safety boundary described above. See [UPSTREAM.md](UPSTREAM.md) for the pinned provenance.

## Overview

The server gives MCP clients a typed interface to monitor and manage AsusWRT routers. It operates exclusively over SSH using allowlisted operations: no arbitrary command execution, no firmware modifications and no factory-reset capability.

## Features

See the complete [tool reference](docs/tools.md) for every tool, access classification, inputs and mutation semantics.


### Read-Only Monitoring (55 tools)

| Category | Tools |
|----------|-------|
| **Identity & Health** | Router model, firmware version, firmware update status, uptime, load, memory |
| **Network** | LAN/WAN details, Dual-WAN status, VLAN/guest segmentation, DNS config, DNS Privacy/DNSSEC status, IPv6 status, routing table, QoS status, sanitized traffic-monitoring posture |
| **Clients** | Connected clients, DHCP leases, ARP neighbors |
| **Wireless** | Radio status, SSIDs, guest networks, WPS state, Smart Connect/roaming, advanced radio features, sanitized per-radio scheduling state, client counts per band, AiMesh status |
| **Services** | Running processes, open ports, cron jobs, sanitized local/remote syslog posture, auxiliary FTP/media/WebDAV/cloud/modem/printer/legacy-VPN posture |
| **Storage** | USB devices, mounts, partitions, filesystem usage |
| **Security** | Firewall posture, port-trigger/DMZ/NAT-passthrough state, UPnP, DDNS, Samba status, conntrack usage, AiProtection status |
| **VPN** | OpenVPN server, WireGuard, sanitized VPN client slot/profile counts and VPN Fusion policy counts |
| **Administration** | Web admin ports, SSH/telnet access settings |
| **Diagnostics** | SSH TCP/banner/auth diagnostics, config snapshot |

### Mutation Tools (with safety guards)

All mutation tools require:
- `confirm: true` parameter
- `ASUSWRT_ALLOW_MUTATIONS=true` environment variable
- Support for `dry_run: true` to preview changes

| Tool | Description |
|------|-------------|
| `asuswrt_restart_service` | Restart allowlisted services (httpd, firewall, wireless, dnsmasq, etc.) |
| `asuswrt_dhcp_server` | Enable/disable DHCP server |
| `asuswrt_upnp` | Enable/disable UPnP |
| `asuswrt_radio` | Enable/disable Wi-Fi radio bands |
| `asuswrt_guest_wifi` | Enable/disable guest Wi-Fi |
| `asuswrt_guest_lan_access` | Toggle LAN access for guest Wi-Fi |
| `asuswrt_port_forwarding` | List, add, remove, enable/disable port forwarding rules |
| `asuswrt_vpn_server` | Enable/disable OpenVPN server |
| `asuswrt_wireguard_client` | Connect/disconnect/restart an already-configured WireGuard client slot |
| `asuswrt_parental_access` | List, block, unblock, remove parental control rules |
| `asuswrt_parental_block_all` | Toggle block-all mode |
| `asuswrt_dhcp_reservation` | List, add, remove DHCP static reservations |

### Safety Model

- **No arbitrary SSH**: Only allowlisted commands are executed via NVRAM and service calls
- **No firmware operations**: No flash, reset, or bootloader access
- **Secret redaction**: Passwords and sensitive data are never exposed in tool responses
- **Dry-run support**: Every mutation can be previewed before applying
- **Confirmation required**: Mutations require explicit `confirm=True`
- **SSH-only transport**: No exposure of the router's web API

## Feedback and contributions

Use GitHub Issues for bug reports and feature requests after publication, and pull requests for proposed changes. See [CONTRIBUTING.md](CONTRIBUTING.md). Security issues must follow [SECURITY.md](SECURITY.md), and release changes are summarized in [CHANGELOG.md](CHANGELOG.md).

## Prerequisites

- Python 3.11+
- An AsusWRT or AsusWRT-Merlin router with SSH access enabled
- Network connectivity from the MCP client to the router

## Compatibility

The maintained repository verifier tests the complete source contract on **Python 3.11** and **Python 3.13**. The accepted local runtime uses Python 3.12, so the current 3.11-3.13 interpreter range is exercised across verification and deployment.

Live router acceptance for `v0.2.0` has been performed against a stock ASUSWRT runtime that identifies itself as **XT8PRO** with firmware **388_24854-g9c246e8**. The implementation also preserves upstream AsusWRT-Merlin compatibility assumptions where they remain valid, but this project does **not** claim that all ASUS router models or all AsusWRT/AsusWRT-Merlin firmware versions have been tested. Use the documented safety guards and validate behavior on other firmware families before relying on mutation tools.

## Installation

### 1. Clone and setup

```bash
git clone https://github.com/X1pheR/asuswrt-mcp.git
cd asuswrt-mcp

# Create virtual environment
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Configure environment

```bash
# Copy example configuration
cp .env.example .env

# Edit with your router credentials
# Use your favorite editor:
notepad .env        # Windows
nano .env           # Linux/macOS
```

### 3. Configure `.env`

```env
# Required: Router connection
ASUSWRT_HOST=192.168.1.1
ASUSWRT_SSH_USERNAME=admin

# Choose one SSH authentication method; key authentication is recommended.
ASUSWRT_SSH_KEY_FILE=~/.ssh/id_ed25519
# ASUSWRT_SSH_PASSWORD=your_password

# Optional: Enable mutations (disabled by default)
# ASUSWRT_ALLOW_MUTATIONS=true

# Optional: Connection settings
# ASUSWRT_SSH_PORT=22
# ASUSWRT_TIMEOUT_SECONDS=10
```

## Usage

### Run the MCP server

```bash
# Standard stdio mode
python -m asuswrt_mcp.server

# Or use the entry point
asuswrt-mcp
```

### Configure in Claude Desktop / Cursor

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "asuswrt-mcp": {
      "command": "C:\\path\\to\\asuswrt-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "asuswrt_mcp.server"],
      "env": {
        "ASUSWRT_HOST": "192.168.1.1",
        "ASUSWRT_SSH_USERNAME": "admin",
        "ASUSWRT_SSH_PASSWORD": "your_password"
      }
    }
  }
}
```

### Using with npx Inspector (development)

```bash
npx @modelcontextprotocol/inspector python -m asuswrt_mcp.server
```

## Development

Run the canonical local verification gate:

```bash
./scripts/verify.sh
```

This runs the maintained compatibility tests, builds wheel/sdist artifacts and performs the HIGH/CRITICAL dependency, secret and misconfiguration scan. See [CONTRIBUTING.md](CONTRIBUTING.md) for development and safety requirements.

## Project Structure

```
asuswrt-mcp/
├── src/asuswrt_mcp/
│   ├── server.py          # FastMCP entrypoint & tool definitions
│   ├── service.py         # Business logic & router operations
│   ├── config.py          # Settings management
│   ├── clients/
│   │   └── ssh.py         # SSH client wrapper
│   ├── nvram.py           # NVRAM parsing utilities
│   ├── ssh_parsers.py     # Output parsers for SSH commands
│   ├── security.py        # Mutation guards & redaction
│   ├── validators.py      # Input validation
│   ├── responses.py       # Tool response formatting
│   ├── errors.py          # Custom exceptions
│   └── serialization.py   # Safe serialization
├── tests/                 # Unit and release-contract tests
├── .env.example           # Example configuration
├── docs/tools.md          # Complete MCP tool reference
├── scripts/verify.sh      # Canonical local verification gate
├── pyproject.toml         # Project metadata
└── README.md              # This file
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [asusrouter](https://pypi.org/project/asusrouter/) for the underlying Python library
- [MCP](https://modelcontextprotocol.io/) for the protocol specification
- [AsusWRT-Merlin](https://asuswrt-merlin.net/) for the firmware