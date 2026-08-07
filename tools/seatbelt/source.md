# Seatbelt

- **Repo:** https://github.com/GhostPack/Seatbelt
- **Pinned ref:** `392171df84472591d4eae7ebd5b1cdc96ba91377` (`master`, checked 2026-08-06)
- **License:** BSD 3-Clause

## Why this ref

GhostPack tools don't cut versioned tags, so we pin to a specific commit on
`master` rather than tracking the branch head, for the same
reproducibility reason every other tool here is pinned: anyone can check
out that exact ref and diff it against what CI compiled.

## How it's built

See [`build-seatbelt.yml`](../../.github/workflows/build-seatbelt.yml).
GitHub Actions clones this exact ref, restores NuGet packages and compiles
`Seatbelt.sln` (Release|Any CPU, .NET Framework 3.5) with MSBuild on a
Windows runner, hashes the resulting binary, and publishes it as a signed
Release asset with build provenance attestation.
