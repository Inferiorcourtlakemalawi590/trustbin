# GodPotato

- **Repo:** https://github.com/BeichenDream/GodPotato
- **Pinned ref:** `59f66583474fb0297b7447551460e1072de324c0` (`master`, checked 2026-08-06)
- **License:** Apache-2.0

## Why this ref

Upstream's newest tag (`V1.20`, 2023-04-11) is 7 commits behind `master`,
which includes real fixes since (system user detection, multi-exploit
support, updated SharpToken) and was never re-tagged. We pin past the tag
to `59f66583` (`master` HEAD as of 2026-08-06) to get those fixes - see
[README.md § Pinning past the latest tag](../../README.md#pinning-past-the-latest-tag)
for when/why this repo does that. Pinned to the exact commit rather than
tracking the branch for the same reproducibility reason every other tool
here is pinned: anyone can check out that exact ref and diff it against
what CI compiled.

## How it's built

See [`build-godpotato.yml`](../../.github/workflows/build-godpotato.yml).
GitHub Actions clones this exact ref and compiles `GodPotato.csproj` with
MSBuild on a Windows runner. Upstream's csproj declares
`<OutputType>Library</OutputType>` targeting .NET Framework 2.0 (it's
normally consumed as a loaded assembly), so the workflow overrides
`OutputType=Exe` at the MSBuild command line to produce a standalone
`GodPotato.exe`, matching how the tool is documented and commonly used
upstream. The source file itself is never modified. CI hashes the resulting
binary and publishes it as a signed Release asset with build provenance
attestation.
