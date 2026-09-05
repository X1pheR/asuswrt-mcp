# Security policy

## Supported version

Security fixes target the latest released version. Before the first public release, the current release candidate is supported only for local evaluation.

## Reporting a vulnerability

After publication, use GitHub's **private vulnerability reporting / Security Advisory** flow for this repository when available. Please include the affected version, impact, reproduction steps and any suggested mitigation, but never include real router credentials, private keys, Wi-Fi PSKs or VPN key material.

If private vulnerability reporting is unavailable, open a public issue containing **only** the title `Security contact request` and a request for a private reporting channel. Do not include vulnerability details, exploit steps, credentials or private infrastructure information in that issue.

## Security boundary

This MCP deliberately excludes arbitrary SSH commands, arbitrary NVRAM access, firmware flashing/reset, bootloader operations and generic HTTP passthrough. Router mutations are disabled by default and require both `ASUSWRT_ALLOW_MUTATIONS=true` and explicit `confirm=true`; supported management tools also provide `dry_run=true`.
