# Changelog

All notable downstream changes are recorded here.

## [0.2.0] - Unreleased

### Added

- Expanded the MCP surface from the pinned upstream baseline of 47 tools to 67 tools: 55 read tools and 12 management tools.
- Added 19 sanitized read tools covering firewall posture, Wi-Fi radio configuration/scheduling, DNS Filter/Privacy, QoS, AiProtection, AiMesh, VLAN/guest segmentation, Dual-WAN, WPS, Smart Connect/roaming, firmware-update status, VPN-client health, WAN watchdog, logging, traffic-monitoring posture and auxiliary-service posture.
- Added bounded connect/disconnect/restart management for already-configured WireGuard client slots.
- Added a complete public tool reference and repository-owned local release verifier.

### Fixed

- Treat ASUS `sshd_enable=2` as SSH enabled.
- Detect configured/enabled WireGuard clients when legacy VPN-client profile data is absent.
- Delimit bulk NVRAM reads explicitly so empty values cannot corrupt the following key/value record.

### Security

- Keep sensitive VPN, DNS, Wi-Fi and policy data outside model-visible responses where sanitized state/count metadata is sufficient.
- Refreshed the dependency lock to remove known HIGH/CRITICAL findings in the release candidate and raised the direct MCP SDK floor to `>=1.29.1`.
- Moved to the official Paramiko 5.x release line, which contains the SHA-1 removal previously consumed through a pinned pre-release Git commit.
