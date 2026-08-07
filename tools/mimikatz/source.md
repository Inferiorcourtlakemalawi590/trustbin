# mimikatz

- **Repo:** https://github.com/gentilkiwi/mimikatz
- **Pinned ref:** `306bc6b43099c7b698f2898401fddbded6a630c8` (`master`, checked 2026-08-07)
- **License:** CC BY 4.0

## Why this ref

Upstream's newest tag (`2.2.0-20220919`) is from 2022-09-19; `master` has
kept moving since with no new tag, so we pin to the exact `master` HEAD
instead - see
[README.md § Pinning past the latest tag](../../README.md#pinning-past-the-latest-tag).
Pinned to a specific commit rather than tracking the branch for the same
reproducibility reason every other tool here is pinned: anyone can check
out that exact ref and diff it against what CI compiled.

## How it's built

See [`build-mimikatz.yml`](../../.github/workflows/build-mimikatz.yml).
GitHub Actions clones this exact ref and compiles only the `mimikatz`
project (`mimikatz/mimikatz.vcxproj`, Release, Win32 and x64) with MSBuild
on a Windows runner, then runs the resulting binary non-interactively to
confirm it actually starts, not just that it compiled. The full
`mimikatz.sln` also includes `mimidrv` (a kernel driver) and `mimilove`,
both of which need the Windows Driver Kit 7.1; upstream's own README
states `mimikatz` and `mimilib` build fine without it, so the workflow
targets the `mimikatz` project directly instead of the whole solution.
Hashes the resulting binaries and publishes them as signed Release assets
with build provenance attestation.

Three adjustments are needed to build `mimikatz.vcxproj` directly on a
current runner, none of which touch the tool's actual logic:

- The project forces `PlatformToolset` to a Windows-XP-compatible value
  no longer shipped by Visual Studio. The workflow strips those lines
  from the checked-out project file (CI workspace only, not upstream).
- With no explicit toolset, MSBuild's default resolution still lands on
  an unavailable value, so the workflow detects the toolset actually
  installed on the runner and passes it explicitly.
- `IncludePath` depends on `$(SolutionDir)`, normally set only when
  building through `mimikatz.sln`. The workflow passes it explicitly
  since it builds the `.vcxproj` directly, to avoid `mimidrv`.

The resulting binary links its C runtime statically (no `VCRUNTIME`,
`MSVCP`, or `ucrtbase` dependency), so it runs without a separately
installed Visual C++ Redistributable.
