# SharPersist

- **Repo:** https://github.com/mandiant/SharPersist
- **Pinned ref:** `01fb8bb22cdea29f6d0dce2fd28698f4edfffdb9` (`master`, checked 2026-08-06)
- **License:** See upstream repo (Mandiant/FireEye; repo is publicly
  archived but this is the official, canonical location)

## Why this ref

This repo doesn't track a moving branch beyond its last commit (it's
archived upstream), and the newest tagged release (v1.0.1) predates this
commit, so we pin to the exact HEAD commit for full reproducibility:
anyone can check out that exact ref and diff it against what CI compiled.

## How it's built

See [`build-sharpersist.yml`](../../.github/workflows/build-sharpersist.yml).
GitHub Actions clones this exact ref, restores NuGet packages and compiles
`SharPersist.sln` with MSBuild on a Windows runner, hashes the resulting
binary, and publishes it as a signed Release asset with build provenance
attestation.

Upstream's csproj targets .NET Framework v4.0 (Release|Any CPU), but
`windows-latest` runners only ship targeting packs for 4.5+ (4.0 was
superseded in-place by those, so Microsoft doesn't redistribute a separate
4.0 pack for current toolchains - `MSB3644: reference assemblies ... were
not found`). The workflow overrides `TargetFrameworkVersion=v4.7.2` at the
MSBuild command line to build against a pack that's actually installed;
4.0-era code builds fine against it since 4.5+ is an in-place,
backward-compatible upgrade. The source file itself is never modified.

Upstream also doesn't ship a `packages.config` anywhere in the repo at
this ref, even though `SharPersist.csproj` references two NuGet packages
by `HintPath` (`..\packages\<pkg>.<version>\lib\net40\...`): `Costura.Fody`
3.3.3 and `TaskScheduler` 2.8.11. `nuget restore` on the `.sln` silently
finds nothing to do, so the workflow installs both packages explicitly
into that exact expected layout instead.
