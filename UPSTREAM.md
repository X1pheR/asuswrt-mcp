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

## Mandatory trusted SSH host identity upstream contribution

Upstream default in official teefloo/asuswrt-mcp master was
paramiko.AutoAddPolicy(), with ssh_strict_host_key=false.
The official SSH implementation already passes
look_for_keys=False and allow_agent=False, so no upstream patch
is needed for implicit agent/key lookup.
Local AS-P03 commit f86b830 enforces fail-closed known-host
validation and removes the insecure bypass.

[Issue #5](https://github.com/teefloo/asuswrt-mcp/issues/5)
and [draft PR #6](https://github.com/teefloo/asuswrt-mcp/pull/6)
now carry a targeted upstream-native version of that policy,
based on master 46516892cade39177327d404fed09d91b1a3a8dd
at head 1d324f5d0568e7f223cebac45f44e61d19e8cf6c.
The new host-key policy regression failed on original source
and passed after the change; all 70 router-independent upstream
Python unit tests and the lockfile check passed.
The PR removes the optional insecure host-key bypass and
documents known_hosts pretrust, which affects first-use
compatibility and needs maintainer review and representative
live-router acceptance before source/release adoption.

## Transitive dependency upstream contribution

An independent maintained downstream source commit ce3ae38 refreshed
the retained transitive PyJWT and urllib3 lockfile entries.
After checking upstream issues and PRs, the official upstream
[issue #2](https://github.com/teefloo/asuswrt-mcp/issues/2)
and [draft PR #4](https://github.com/teefloo/asuswrt-mcp/pull/4)
now track the generic change against upstream master
46516892cade39177327d404fed09d91b1a3a8dd.
The exact PR HEAD is
5eb17316c371c4520df71e5fb55535e3f82c680e.
The official upstream source passed uv lock --check --offline
and 69 unit tests on the exact patch, plus git diff --check.
Only uv.lock changes; no router runtime is modified.

X1pheR/asuswrt-mcp is an independently maintained downstream
repository, not registered as a fork of the upstream repository on GitHub.
An earlier direct cross-repository PR attempt failed GitHub head validation;
temporary fork-local PR #15 was closed unmerged.
A separate actual GitHub contribution fork,
X1pheR/asuswrt-mcp-1, was then created without renaming,
re-parenting or modifying the existing maintained repository.
Its branch contains only this upstream-native tested change.
A draft upstream PR does not prove merge or official release inclusion;
do not remove the patch until upstream release adoption and
representative dependency and router compatibility acceptance.

## Machine-readable downstream patch register

This inline register is the product-owned logical-patch projection used by SDLC-09 structural verification. Its state does not replace current GitHub issue/PR verification, an actual upstream-compatible tested diff, or any required operator-approved product ADR. Unlinked rows are explicitly nonconformant; no historical fork behavior has been grandfathered. Cross-product integration and release actions remain gated separately. Patch scope and local commit mappings require further semantic review before external contribution.

<!-- SDLC-UPSTREAM-REGISTER:1 -->
```json
{
  "schema_version": 1,
  "upstream": "teefloo/asuswrt-mcp",
  "baseline": "46516892cade39177327d404fed09d91b1a3a8dd",
  "patches": [
    {
      "id": "AS-P01",
      "kind": "upstream",
      "scope": "Broader sanitized read-only SSH router observability beyond official upstream",
      "local_commits": [
        "6fff61f"
      ],
      "checked_on": "2026-11-11",
      "issue": "https://github.com/teefloo/asuswrt-mcp/issues/11",
      "pr": "https://github.com/teefloo/asuswrt-mcp/pull/12",
      "pr_state": "draft"
    },
    {
      "id": "AS-P02",
      "kind": "upstream",
      "scope": "Syslog management and verification including active-vs-stored state and complete logger arguments",
      "local_commits": [
        "fbe85a0",
        "cb88615",
        "794ad24",
        "57635d5"
      ],
      "checked_on": "2026-11-11",
      "issue": "https://github.com/teefloo/asuswrt-mcp/issues/7",
      "pr": "https://github.com/teefloo/asuswrt-mcp/pull/8",
      "pr_state": "draft"
    },
    {
      "id": "AS-P03",
      "kind": "upstream",
      "scope": "Mandatory known-host SSH router identity verification (upstream already disables implicit ssh-agent and key search)",
      "local_commits": [
        "f86b830"
      ],
      "checked_on": "2026-11-11",
      "issue": "https://github.com/teefloo/asuswrt-mcp/issues/5",
      "pr": "https://github.com/teefloo/asuswrt-mcp/pull/6",
      "pr_state": "draft"
    },
    {
      "id": "AS-P04",
      "kind": "upstream",
      "scope": "Transitive vulnerable dependency security updates",
      "local_commits": [
        "ce3ae38"
      ],
      "checked_on": "2026-11-11",
      "issue": "https://github.com/teefloo/asuswrt-mcp/issues/2",
      "pr": "https://github.com/teefloo/asuswrt-mcp/pull/4",
      "pr_state": "draft"
    },
    {
      "id": "AS-P05",
      "kind": "distribution",
      "scope": "Temporary X1pheR release version and image/publication workflow needed while tracked ASUS source fixes await official upstream artifacts",
      "local_commits": [
        "31b543a"
      ],
      "checked_on": "2026-11-11",
      "temporary": true,
      "depends_on": [
        "AS-P01",
        "AS-P02",
        "AS-P03",
        "AS-P04",
        "AS-P06",
        "AS-P07"
      ],
      "exit_when": "Official upstream artifact includes the linked fixes, and source verification plus router/consumer and rollback acceptance establish that the own release identity and workflow can be retired."
    },
    {
      "id": "AS-P06",
      "kind": "upstream",
      "scope": "Explicitly confirmed, bounded operations on existing WireGuard client slots 1..5",
      "local_commits": [
        "6fff61f"
      ],
      "checked_on": "2026-11-11",
      "issue": "https://github.com/teefloo/asuswrt-mcp/issues/9",
      "pr": "https://github.com/teefloo/asuswrt-mcp/pull/10",
      "pr_state": "draft"
    },
    {
      "id": "AS-P07",
      "kind": "upstream",
      "scope": "Security lockfile refresh for aiohttp, certifi and required yarl resolver update",
      "local_commits": [
        "4effea7554d7c48619ef15f029c8a574123fc2dd"
      ],
      "checked_on": "2026-11-11",
      "issue": "https://github.com/teefloo/asuswrt-mcp/issues/13",
      "pr": "https://github.com/teefloo/asuswrt-mcp/pull/14",
      "pr_state": "open"
    }
  ]
}
```

## ASUS remote syslog upstream convergence

AS-P02: official upstream issue [#7](https://github.com/teefloo/asuswrt-mcp/issues/7)
and draft [PR #8](https://github.com/teefloo/asuswrt-mcp/pull/8), exact
head b4ff566ee691d5dbeb80ba0d180a2c8e4308d864 on upstream master.
The retained remote-syslog implementation and nine source regression
test functions were ported into the upstream tool/service/fake SSH owner.
Local upstream test command passed; real router acceptance, maintainer CI,
merge and immutable official release inclusion are not yet established.
No downstream product source/publication or router runtime was changed.

## WireGuard source contribution

A combined preliminary AS-P01 grouping has been split into
AS-P01 sanitized observability and AS-P06 bounded WireGuard management
because these are independent upstream behaviors. AS-P06 is tracked
by [issue #9](https://github.com/teefloo/asuswrt-mcp/issues/9)
and [draft PR #10](https://github.com/teefloo/asuswrt-mcp/pull/10),
exact head 15b5ee7cdc6745681dbfbb1f05bac66aa73c60d7.
The upstream candidate includes read-only/dry-run and explicit mutation
contracts for configured client slots; 75 upstream tests passed.
Maintainer review, official release inclusion and any live router
acceptance are still pending. No downstream promotion occurred.

## Read-only router observability upstream contribution

AS-P01 now links to official
[issue #11](https://github.com/teefloo/asuswrt-mcp/issues/11) and
[draft PR #12](https://github.com/teefloo/asuswrt-mcp/pull/12),
head a114a9d89507a5b6f73a16e82a0450c244f72753. Source-only
router read status, redaction and fake-SSH regressions ported against
upstream master 46516892cade39177327d404fed09d91b1a3a8dd;
the exact complete upstream unit suite passed 103 tests.
AS-P02 remote syslog and AS-P06 WireGuard management remain separate
source contributions; PR #12 deliberately excludes their mutations.
All submitted upstream ASUS PRs are draft/unmerged. No local
maintained release, official immutable adoption or live router
acceptance occurred. AS-P05 is a temporary distribution record tied to the five linked upstream source patches; downstream release/adoption remains separately gated.

## Convergence lifecycle

Verify existing upstream issues and PRs, current default-branch equivalence, and source-owned regression evidence before submitting missing contributions. A PR that is closed without merge is nonconformant, and a merged PR is not automatically present in an immutable official release. Remove a downstream patch only on a tested candidate against a suitable released upstream artifact. Retire the fork only after verified patch elimination, accepted distribution/ADR disposition, rollback readiness, consumer parity, and separate operator approval for production/retirement.


## Temporary distribution exit — AS-P05

Release-only identity and publication are temporary dependencies of the tracked source patches above, not a product divergence or an upstream contribution. The existing source verifier remains ordinary product-owned verification, not an exempt patch. Reassess removal after immutable upstream release and separately authorized consumer/rollback acceptance. No deployment or release is authorized by this register.
