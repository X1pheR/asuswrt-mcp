# Security policy

## Supported version

Security fixes target the latest released version. Before the first public release, the current release candidate is supported only for local evaluation.

## Reporting a vulnerability

After publication, use GitHub's **private vulnerability reporting / Security Advisory** flow for this repository when available. Please include the affected version, impact, reproduction steps and any suggested mitigation, but never include real router credentials, private keys, Wi-Fi PSKs or VPN key material.

If private vulnerability reporting is unavailable, contact the maintainer through the [GitHub profile associated with this repository](https://github.com/X1pheR) and request a private reporting channel. Do not post vulnerability details, exploit steps, credentials or private infrastructure information publicly.

## Security boundary

This MCP deliberately excludes arbitrary SSH commands, arbitrary NVRAM access, firmware flashing/reset, bootloader operations and generic HTTP passthrough. Router mutations are disabled by default and require both `ASUSWRT_ALLOW_MUTATIONS=true` and explicit `confirm=true`; supported management tools also provide `dry_run=true`. Router SSH connections always require a pre-trusted host key from the local SSH host-key store; unknown or changed host keys are rejected and are never learned automatically.

## Public build and supply-chain boundary

Public GitHub workflows use synthetic/local test fixtures only and must not receive router credentials, SSH private keys, Homelab deployment credentials or production control-plane access. The canonical repository verifier runs before release publication, dependencies are locked, GitHub Actions are pinned to immutable commit SHAs, and release artifacts are built reproducibly with checksums and GitHub/Sigstore provenance.

After the repository becomes public, GitHub-native dependency alerts, secret scanning and push protection, CodeQL/default code scanning where supported, OpenSSF Scorecard results and release immutability must be reviewed as part of the public release gate.
