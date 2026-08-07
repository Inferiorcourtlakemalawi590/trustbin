# PowerLurk

- **Repo:** https://github.com/Sw4mpf0x/PowerLurk
- **Pinned ref:** `ddfa8fb02ddbc19469fdc5314fd764d0a801fbce` (`master`, checked 2026-08-06)
- **License:** None declared upstream (no LICENSE file in the repo as of
  the pinned ref). Treat as "all rights reserved" by the author
  unless/until upstream adds one.

## Why this ref

Upstream doesn't cut tagged releases, so we pin to a specific `master`
commit rather than tracking the branch head, for the same reproducibility
reason every other tool here is pinned: anyone can check out that exact ref
and diff it against what CI published. Confirmed this is the original
author's repo (Andrew Luke / Sw4mpf0x), not one of the several unofficial
forks/mirrors that also exist.

## How it's built

See [`build-powerlurk.yml`](../../.github/workflows/build-powerlurk.yml).
PowerLurk is a PowerShell module, not a compiled binary, so there's no
build step: GitHub Actions clones this exact ref, zips the source tree
as-is, hashes the archive, and publishes it as a signed Release asset with
build provenance attestation. This matches the trust model for every other
tool in this repo: integrity (checksum) + provenance (attestation tying the
archive to the exact upstream ref and the CI run that packaged it).
