# PowerSharpPack

- **Repo:** https://github.com/S3cur3Th1sSh1t/PowerSharpPack
- **Pinned ref:** `c0c7f6f9f775a02e1c86e543afcabfba4aa7e887` (`master`, checked 2026-08-06)
- **License:** None declared upstream (no LICENSE file in the repo as of
  the pinned ref). Treat as "all rights reserved" by the author
  unless/until upstream adds one. Note the pack itself bundles PowerShell
  loaders for several other GhostPack-style C# tools already mirrored
  separately in this repo (Rubeus, Seatbelt, etc.). Check each tool's own
  upstream license before redistributing further.

## Why this ref

Upstream doesn't cut tagged releases, so we pin to a specific `master`
commit rather than tracking the branch head, for the same reproducibility
reason every other tool here is pinned: anyone can check out that exact ref
and diff it against what CI published.

## How it's built

See [`build-powersharppack.yml`](../../.github/workflows/build-powersharppack.yml).
PowerSharpPack is a set of PowerShell loader scripts (with bundled
base64/precompiled binaries), not something this repo compiles itself, so
there's no build step: GitHub Actions clones this exact ref, zips the
source tree as-is, hashes the archive, and publishes it as a signed Release
asset with build provenance attestation. This matches the trust model for
every other tool in this repo: integrity (checksum) + provenance
(attestation tying the archive to the exact upstream ref and the CI run
that packaged it).
