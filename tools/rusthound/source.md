# RustHound-CE

- **Repo:** https://github.com/g0h4n/RustHound-CE
- **Pinned ref:** `v2.4.92` (update this line whenever the workflow is bumped to a new tag)
- **License:** GPL-3.0 (check upstream repo for current terms)

## Why this tag

We pin to a specific tag/commit rather than `main` so every build is
reproducible and auditable: anyone can check out that exact ref and diff
it against what our CI compiled.

## How it's built

See [`build-rusthound.yml`](../../.github/workflows/build-rusthound.yml).
GitHub Actions clones this exact ref, compiles with `cargo build
--release`, hashes the resulting binary, and publishes it as a signed
Release asset with build provenance attestation.

To bump the version: update the ref below AND in the workflow input, open
a PR, let CI build it, verify the diff, then merge + tag a release.
