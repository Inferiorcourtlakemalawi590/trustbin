# LaZagne

- **Repo:** https://github.com/AlessandroZ/LaZagne
- **Pinned ref:** `v2.4.7` (update whenever the workflow is bumped to a new tag)
- **License:** LGPL-3.0

## Why this tag

Pinned to a specific tag rather than `master` so every build is
reproducible: anyone can check out that exact ref and diff it against what
CI compiled.

## How it's built

See [`build-lazagne.yml`](../../.github/workflows/build-lazagne.yml).
GitHub Actions clones this exact ref, packages it with PyInstaller into a
standalone Windows executable, hashes the result, and publishes it as a
signed Release asset with build provenance attestation.

## Note

LaZagne is a credential-dumping tool. Expect antivirus / EDR products to
flag it. That's expected behavior for this class of tool, not evidence of
tampering. Verify via checksum + attestation, not via AV status.
