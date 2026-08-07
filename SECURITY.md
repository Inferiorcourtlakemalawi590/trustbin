# Reporting an issue

## A binary looks suspicious or doesn't match its published checksum

Open an issue immediately with:

- The exact filename and download URL.
- The output of `sha256sum <file>`.
- The output of `gh attestation verify <file> -R <owner>/trustbin`.

Any binary that fails verification will be removed from the affected
release without delay.

## Vulnerability in the build pipeline

If you find a flaw in a workflow (e.g. a possible code-injection path
during build, or a supply-chain issue with a dependency), please report
it via a private GitHub security advisory rather than a public issue.
