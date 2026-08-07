# Chisel

- **Repo:** https://github.com/jpillora/chisel
- **Pinned ref:** `v1.11.8` (update whenever the workflow is bumped to a new tag)
- **License:** MIT

## Why this tag

Pinned to a specific tag rather than `main` so every build is reproducible:
anyone can check out that exact ref and diff it against what CI compiled.

## How it's built

See [`build-chisel.yml`](../../.github/workflows/build-chisel.yml).
GitHub Actions clones this exact ref, compiles with `go build`, hashes the
resulting binaries (Linux + Windows, amd64), and publishes them as a signed
Release asset with build provenance attestation.
