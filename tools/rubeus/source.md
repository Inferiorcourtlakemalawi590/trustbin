# Rubeus

- **Repo:** https://github.com/GhostPack/Rubeus
- **Pinned ref:** `1.6.4` (tag `e93119a371606fae56fd63f0d285f3773287394d`)
- **License:** BSD 3-Clause

## Why this tag

Rubeus does cut occasional tagged releases; we pin to the latest one
(1.6.4) rather than the `master` branch head so every build is
reproducible: anyone can check out that exact ref and diff it against what
CI compiled.

## How it's built

See [`build-rubeus.yml`](../../.github/workflows/build-rubeus.yml).
GitHub Actions clones this exact ref, restores NuGet packages and compiles
`Rubeus.sln` (Release|Any CPU, .NET Framework 4.0) with MSBuild on a
Windows runner, hashes the resulting binary, and publishes it as a signed
Release asset with build provenance attestation.
