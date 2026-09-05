## Summary

Describe the bounded change and why it belongs in ASUSWRT MCP.

## Verification

- [ ] `./scripts/verify.sh` passes locally.
- [ ] Functional changes add or update automated tests where practical.
- [ ] MCP/tool contract changes update `docs/tools.md` and tool counts.
- [ ] User-visible changes update `CHANGELOG.md`.

## Security and router boundary

- [ ] No router credential, SSH private key, Wi-Fi PSK, VPN key/peer/endpoint, private network inventory or private deployment detail is included.
- [ ] The change does not add arbitrary SSH, arbitrary NVRAM access, firmware/reset capability or generic HTTP passthrough.
- [ ] Mutations remain bounded, disabled by default, dry-run capable and explicitly confirmed.
- [ ] Sensitive read output remains data-minimized and any changed trust boundary has negative/regression coverage.
