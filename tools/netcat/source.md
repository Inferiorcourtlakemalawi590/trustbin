# netcat

- **Repo:** https://github.com/diegocr/netcat (diegocr fork, widely used single-file C implementation)
- **Pinned ref:** `7c1219817a9ce483dfb646f0bbe33537240303eb` (`master`, checked 2026-08-06)
- **License:** See upstream repo (BSD-style / public domain original netcat)

## Why this source

There is no single canonical "netcat" upstream; this fork is a common,
actively referenced single-file C implementation that builds cleanly with
both gcc (Linux) and mingw (Windows), which keeps the CI build simple and
auditable. If you need a specific variant (OpenBSD nc, GNU netcat, Nmap's
ncat), open an issue. Those can be added as separate, clearly labeled tools
rather than conflated under one name.

## How it's built

See [`build-netcat.yml`](../../.github/workflows/build-netcat.yml).
GitHub Actions clones this exact ref, compiles with gcc (Linux) and
mingw-w64 (Windows), hashes the resulting binaries, and publishes them as a
signed Release asset with build provenance attestation.

## Note on GAPING_SECURITY_HOLE

Built without `-DGAPING_SECURITY_HOLE` (the `-e` / remote command exec
flag). Upstream itself gates that behind an opt-in build define because of
the risk it carries, and enabling it also breaks the Windows build: its
`doexec()` Windows implementation lives in a companion `doexec.c` that this
single-file mirror doesn't ship, so the linker fails. Core netcat (connect,
listen, port scan, file transfer via redirection) doesn't need it. If you
specifically need `-e` support, build it yourself from source with that
flag and accept the risk.

## Other build quirks (Linux only)

This mirror's `netcat.c` has a couple of rough edges that only show up
when building for Linux (it was clearly written Windows-first):

- `HAVE_BIND` is hardcoded on, which pulls in a call to `res_init()`.
  Linking `-lresolv` doesn't reliably resolve this on modern glibc
  (libresolv was folded into libc), and the call isn't needed since glibc
  initializes the resolver lazily on its own anyway. Stubbed to a no-op via
  `-Dres_init()=(0)`.
- The `d` (detach from console) switch case calls the Win32-only
  `FreeConsole()` with no `#ifdef WIN32` guard, so it has to resolve on
  every platform. Fixed by stubbing it to a no-op via a compiler define
  (`-DFreeConsole()=((void)0)`), which is also just correct behavior on
  Linux.
- `O_WRONLY`/`O_CREAT`/`O_TRUNC` are used without including `fcntl.h`.
  Fixed with `-include fcntl.h`.

All three are compiler/linker flags applied in the workflow, the source
file itself is never modified.
