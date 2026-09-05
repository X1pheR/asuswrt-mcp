# Contributing

`asuswrt-mcp` is a maintained downstream of [`teefloo/asuswrt-mcp`](https://github.com/teefloo/asuswrt-mcp). Contributions should preserve the explicit, bounded MCP surface rather than introduce generic SSH, NVRAM or HTTP escape hatches.

## Development rules

- Add or change behavior test-first when practical.
- Keep read tools data-minimized: do not expose credentials, Wi-Fi PSKs, VPN keys, peer identities/endpoints or raw policy/rule payloads when a sanitized summary is sufficient.
- Every real mutation must remain disabled unless mutations are globally enabled, require explicit confirmation and support dry-run preview.
- New management capabilities must be bounded to a concrete operator use case and include negative safety tests.
- Generic correctness fixes that apply cleanly to upstream are good candidates for a separate upstream contribution.
- Update `docs/tools.md`, README counts and release metadata whenever the MCP contract changes.

## Verification

Run the canonical local gate from the repository root:

```bash
./scripts/verify.sh
```

The verifier tests the supported Python floor and current development baseline, builds wheel/sdist artifacts, and runs the HIGH/CRITICAL Trivy vulnerability/secret/misconfiguration gate.

## Pull requests

Keep changes focused and explain the capability or correctness problem being solved, the safety boundary, tests added and any compatibility assumptions. Never commit real router addresses, usernames, credentials, keys or private deployment paths.
