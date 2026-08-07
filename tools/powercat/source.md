# powercat

- **Repo:** https://github.com/besimorhino/powercat
- **Pinned ref:** `4e33fdfa2850a8940e46d0b69250ae3ba3a8c640` (`master`, checked 2026-08-06)
- **License:** None declared upstream (no LICENSE file in the repo as of
  the pinned ref). Treat as "all rights reserved" by the author
  unless/until upstream adds one.

## Why this ref

Upstream doesn't cut tagged releases, so we pin to a specific `master`
commit rather than tracking the branch head, for the same reproducibility
reason every other tool here is pinned: anyone can check out that exact ref
and diff it against what CI published.

## How it's built

See [`build-powercat.yml`](../../.github/workflows/build-powercat.yml).
powercat is a single PowerShell script, not a compiled binary, so there's
no build step: GitHub Actions clones this exact ref, hashes `powercat.ps1`
directly, and publishes it as a signed Release asset with build provenance
attestation. This matches the trust model for every other tool in this
repo: integrity (checksum) + provenance (attestation tying the file to the
exact upstream ref and the CI run that published it).
