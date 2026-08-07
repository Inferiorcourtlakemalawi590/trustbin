# PowerSploit

- **Repo:** https://github.com/PowerShellMafia/PowerSploit
- **Pinned ref:** `d943001a7defb5e0d1657085a77a0e78609be58f` (`master`,
  checked 2026-08-06; repo is archived upstream but this is the official,
  canonical location)
- **License:** BSD 3-Clause

## Why this ref

Upstream's newest tag (v3.0.0) predates this commit and the repo is now
archived (read-only), so we pin to the exact last `master` commit rather
than the tag, for the same reproducibility reason every other tool here is
pinned: anyone can check out that exact ref and diff it against what CI
published.

## How it's built

See [`build-powersploit.yml`](../../.github/workflows/build-powersploit.yml).
PowerSploit is a collection of PowerShell modules, not a compiled binary,
so there's no build step: GitHub Actions clones this exact ref, zips the
source tree as-is, hashes the archive, and publishes it as a signed Release
asset with build provenance attestation. This matches the trust model for
every other tool in this repo: integrity (checksum) + provenance
(attestation tying the archive to the exact upstream ref and the CI run
that packaged it).
