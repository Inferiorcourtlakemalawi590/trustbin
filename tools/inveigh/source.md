# Inveigh

- **Repo:** https://github.com/Kevin-Robertson/Inveigh
- **Pinned ref:** `7aea2e7213c9e89ad13fb132d048cf589c6a03f7` (`master`, checked 2026-08-06)
- **License:** BSD 3-Clause

## Why this ref

Upstream has tagged releases up to v2.0.9, but this pin tracks a specific
`master` commit past that tag, for the same reproducibility reason every
other tool here is pinned: anyone can check out that exact ref and diff it
against what CI published.

## How it's built

See [`build-inveigh.yml`](../../.github/workflows/build-inveigh.yml).
Inveigh is a set of PowerShell scripts (with an optional C# assembly), not
a single compiled binary, so there's no build step: GitHub Actions clones
this exact ref, zips the source tree as-is, hashes the archive, and
publishes it as a signed Release asset with build provenance attestation.
This matches the trust model for every other tool in this repo: integrity
(checksum) + provenance (attestation tying the archive to the exact
upstream ref and the CI run that packaged it).
