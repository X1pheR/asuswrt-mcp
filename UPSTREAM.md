# Upstream provenance

This project is an **independent downstream** derived from [`teefloo/asuswrt-mcp`](https://github.com/teefloo/asuswrt-mcp). It is maintained as its own product and release line rather than relying on the upstream repository as its release authority.

- Upstream repository: `https://github.com/teefloo/asuswrt-mcp`
- Pinned baseline commit: `46516892cade39177327d404fed09d91b1a3a8dd`
- Baseline date: 2026-04-28
- License: MIT; the upstream copyright and license notice are retained in [LICENSE](LICENSE).

The downstream preserves the upstream allowlisted SSH model while carrying a broader sanitized observability surface, bounded WireGuard client management for already-configured slots, ASUS-specific correctness fixes, and its own release/security verification. Generic fixes that are useful independently can still be proposed upstream; the broader capability and safety boundary remains maintained here.

After the first publication, the intended local Git remote roles are:

- `origin` — the independently maintained `X1pheR/asuswrt-mcp` repository.
- `upstream` — `teefloo/asuswrt-mcp`, retained for provenance, comparison, and selectively integrating relevant upstream changes.

Development remains local-first: upstream changes may be fetched and reviewed locally, but this project does not depend on a platform-level repository relationship to track or integrate them.
