# MailSniper

- **Repo:** https://github.com/dafthack/MailSniper
- **Pinned ref:** `1d5563697105e81faa5825d588362f67549db60a` (`master`, checked 2026-08-06)
- **License:** MIT

## Why this ref

Upstream doesn't cut tagged releases, so we pin to a specific `master`
commit rather than tracking the branch head, for the same reproducibility
reason every other tool here is pinned: anyone can check out that exact ref
and diff it against what CI published.

## How it's built

See [`build-mailsniper.yml`](../../.github/workflows/build-mailsniper.yml).
MailSniper is a PowerShell module, not a compiled binary, so there's no
build step: GitHub Actions clones this exact ref, zips the source tree
as-is, hashes the archive, and publishes it as a signed Release asset with
build provenance attestation. This matches the trust model for every other
tool in this repo: integrity (checksum) + provenance (attestation tying the
archive to the exact upstream ref and the CI run that packaged it).
