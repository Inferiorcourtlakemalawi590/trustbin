# Certify

- **Repo:** https://github.com/GhostPack/Certify
- **Pinned ref:** `b63f21d1be13addc6aebfa145f6a76815c756ddb` (`main`, checked 2026-08-06)
- **License:** BSD 3-Clause

## Why this ref

GhostPack tools don't cut versioned tags, so we pin to a specific commit on
`main` rather than tracking the branch head, for the same reproducibility
reason every other tool here is pinned: anyone can check out that exact ref
and diff it against what CI compiled.

This particular ref is **not** the current `main` HEAD. Upstream's HEAD
(`b723e87...`, merged 2026-07-29) doesn't compile: `Certify/Commands/CertRequest.cs`
calls `CertEnrollment.SendCertificateRequest`/`DownloadCert`/`DownloadAndInstallCert`
with extra `Username`/`Password` arguments that don't exist on those methods
in `Certify/Lib/CertEnrollment.cs` at that ref (`error CS1501: No overload
... takes 4 arguments`). That mismatch was introduced by upstream commit
`922303ff7198` ("Update CertRequest.cs", 2026-07-06) and is still present on
`main` as of this check. We pin to `b63f21d1be13`, the last commit before
that regression, where `Certify.sln` actually builds. Re-check upstream
periodically and bump the ref once it's fixed there.

## How it's built

See [`build-certify.yml`](../../.github/workflows/build-certify.yml).
GitHub Actions clones this exact ref, restores NuGet packages and compiles
`Certify.sln` (Release|Any CPU, .NET Framework 4.7.2) with MSBuild on a
Windows runner, hashes the resulting binary, and publishes it as a signed
Release asset with build provenance attestation.
