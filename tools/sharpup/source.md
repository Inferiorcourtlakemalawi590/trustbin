# SharpUp

- **Repo:** https://github.com/GhostPack/SharpUp
- **Pinned ref:** `8a7579174ed447181835cb82bf2ec0279e9110d0` (`master`, checked 2026-08-06)
- **License:** BSD 3-Clause

## Why this ref

GhostPack tools don't cut versioned tags, so we pin to a specific commit on
`master` rather than tracking the branch head, for the same
reproducibility reason every other tool here is pinned: anyone can check
out that exact ref and diff it against what CI compiled.

## How it's built

See [`build-sharpup.yml`](../../.github/workflows/build-sharpup.yml).
GitHub Actions clones this exact ref, restores NuGet packages and compiles
`SharpUp.sln` (Release|Any CPU, .NET Framework 3.5) with MSBuild on a
Windows runner, hashes the resulting binary, and publishes it as a signed
Release asset with build provenance attestation.
