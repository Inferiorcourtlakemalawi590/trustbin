#!/usr/bin/env python3
"""
Regenerates the shared "latest" release body: a static header plus a
"## Recent builds" changelog, grouped into one collapsible <details>
block per day (newest day first), each entry linking "built from <ref>"
straight to that exact commit/tag on the tool's official upstream repo.

The rendered Markdown *is* the storage: every previous entry is parsed
back out of the current release body (no side file), so there's nothing
else to keep in sync. Only logs a new line when there's something to
say - the tool's first appearance, or its ref changed since the last
entry logged for that tool; an identical rebuild is a no-op.

Two ways to call it:
  - Single build (used by the log-release composite action, one call per
    tool's own release job): env vars TOOL, REF, REPO.
  - Batch (used by build-all's combined publish job): env var
    BUILDS_JSON, a JSON array of {"tool": ..., "ref": ..., "repo": ...}
    objects, applied in order and deduped the same way a sequence of
    single calls would be.

Always needs: GITHUB_REPOSITORY (this repo, for the verify snippet),
GH_TOKEN (for `gh release view`).
"""

import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone

MAX_ENTRIES = 100
MAX_DAY_GROUPS = 15
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

# Entry with a clickable ref (new format): built from [`abc123`](https://github.com/org/repo/tree/<ref>)
LINK_RE = re.compile(
    r"^-\s+\*\*(?P<when>[^*]+)\*\*:?\s*[—-]?\s*`(?P<tool>[^`]+)`:\s*(?P<kind>.+?),"
    r"\s*built from\s*\[`[^`]*`\]\(https://github\.com/(?P<repo>[^/]+/[^/]+)/tree/(?P<ref>[^)]+)\)\s*$"
)
# Legacy entries logged before repo links existed: built from `<ref>`
PLAIN_RE = re.compile(
    r"^-\s+\*\*(?P<when>[^*]+)\*\*:?\s*[—-]?\s*`(?P<tool>[^`]+)`:\s*(?P<kind>.+?),"
    r"\s*built from\s*`(?P<ref>[^`]+)`\s*$"
)
# <summary><b>2026-08-07</b> (n builds)</summary> - the date a day-group's
# entry lines belong to. Entry lines inside a group only carry a
# time-of-day (see render_entry), not the date, so it has to be
# recovered from here while parsing back through the body.
SUMMARY_RE = re.compile(r"^<summary><b>(?P<date>\d{4}-\d{2}-\d{2})</b>")


def parse_line(line):
    line = line.strip()
    m = LINK_RE.match(line)
    if m:
        d = m.groupdict()
        return d
    m = PLAIN_RE.match(line)
    if m:
        d = m.groupdict()
        d["repo"] = None
        return d
    return None


def short_ref(ref):
    return ref[:12] if COMMIT_RE.match(ref or "") else ref


def render_entry(e):
    time_part = e["when"][10:].strip(" :—-") or "?"
    ref_disp = short_ref(e["ref"])
    if e["repo"]:
        ref_md = f"[`{ref_disp}`](https://github.com/{e['repo']}/tree/{e['ref']})"
    else:
        ref_md = f"`{ref_disp}`"
    return f"- **{time_part}**: `{e['tool']}`: {e['kind']}, built from {ref_md}"


def render_log(entries):
    groups = defaultdict(list)
    order = []
    for e in entries:
        date = e["when"][:10]
        if date not in groups:
            order.append(date)
        groups[date].append(e)

    blocks = []
    for date in order[:MAX_DAY_GROUPS]:
        day_entries = groups[date]
        blocks.append("<details>")
        n = len(day_entries)
        blocks.append(f"<summary><b>{date}</b> ({n} build{'s' if n != 1 else ''})</summary>")
        blocks.append("")
        blocks.extend(render_entry(e) for e in day_entries)
        blocks.append("")
        blocks.append("</details>")
        blocks.append("")

    return "\n".join(blocks).rstrip()


def parse_body(old_body):
    """Extracts every existing changelog entry from a release body, newest first."""
    entries = []
    current_date = None
    for raw_line in old_body.splitlines():
        line = raw_line.strip()

        summary_m = SUMMARY_RE.match(line)
        if summary_m:
            current_date = summary_m.group("date")
            continue

        parsed = parse_line(line)
        if not parsed:
            continue

        # Entry lines inside a day-group only carry "HH:MM UTC", not the
        # date - stitch the date from the enclosing <summary> back on.
        # (Genuinely old, pre-grouping entries already have the full date
        # in `when` and are left as-is.)
        if not re.match(r"^\d{4}-\d{2}-\d{2}", parsed["when"]) and current_date:
            parsed["when"] = f"{current_date} {parsed['when']}"

        entries.append(parsed)

    return entries


def log_build(entries, tool, ref, repo):
    """Prepends a new entry for (tool, ref, repo) to `entries` if it's loggable
    (new tool, or ref changed since that tool's last entry) - mutates and
    returns `entries`. A no-op rebuild returns the list unchanged."""
    last = next((e for e in entries if e["tool"] == tool), None)
    if last is None:
        should_log, kind = True, "🆕 new tool"
    elif last["ref"] == ref:
        should_log, kind = False, None
    else:
        should_log, kind = True, "🔄 updated"

    if should_log:
        when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        entries.insert(0, {"when": when, "tool": tool, "kind": kind, "ref": ref, "repo": repo})

    return entries


def main():
    repository = os.environ["GITHUB_REPOSITORY"]

    result = subprocess.run(
        ["gh", "release", "view", "latest", "--repo", repository, "--json", "body", "-q", ".body"],
        capture_output=True,
        text=True,
    )
    old_body = result.stdout if result.returncode == 0 else ""
    entries = parse_body(old_body)

    builds_json = os.environ.get("BUILDS_JSON")
    if builds_json:
        for build in json.loads(builds_json):
            entries = log_build(entries, build["tool"], build["ref"], build["repo"])
    else:
        entries = log_build(entries, os.environ["TOOL"], os.environ["REF"], os.environ["REPO"])

    entries = entries[:MAX_ENTRIES]
    log_md = render_log(entries) if entries else "_(no builds logged yet)_"

    body = f"""Rolling release: every tool's most recently CI-built binaries,
each with its own checksum file (`<tool>-<platform>.sha256`).

For exact provenance of a given asset (upstream ref/commit,
build workflow) see `tools/<tool>/source.md` and this repo's
Actions run history.

Some tools here (e.g. LaZagne) are expected to be flagged by
antivirus/EDR. That's normal for this class of tool, verify
via checksum + attestation, not via AV status.

Verify:
```
sha256sum -c <tool>-<platform>.sha256
gh attestation verify <file> -R {repository}
```

## Recent builds

{log_md}
"""

    with open("release-body.md", "w") as f:
        f.write(body)

    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a") as f:
            f.write("path=release-body.md\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
