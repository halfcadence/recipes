#!/usr/bin/env python3
"""Catch a bare `|` in prose, which kramdown silently turns into a table.

WHY THIS EXISTS. kramdown parses GFM tables, and a table needs no header row and
no delimiter line — a single paragraph containing one `|` is enough. So this line
in changelog.md:

    - **The ultrawide split …** An equal 12&nbsp;|&nbsp;12 spread assumed …

did not render as prose. It rendered as a two-cell <table>, splitting one sentence
across two <td>s at the pipe. Worse, a table cell is its own parse context, so the
`**…**` in `a **name | list pair**` came out with the asterisks PRINTED — the
emphasis never closed inside either cell.

Both shipped and were live for weeks. Nothing failed: the build is green, the HTML
is valid, and the page looks merely a little odd — which is exactly why it went
unnoticed until the colophon pages got a layout that made a stray table obvious.

WHAT THIS CHECKS. Every `|` in a markdown file must be one of:
  · inside a real table (a row whose line starts with `|`, or a `---|---` rule)
  · inside `code`/```fenced``` (a pipe there is content, not markup)
  · inside a Liquid tag or expression — `{{ x | filter }}`, `{%- assign … -%}`
  · written as the entity `&#124;`, which kramdown does not see as a delimiter

Anything else is prose, and prose must escape it: use `&#124;`.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def strip_safe(line: str) -> str:
    """Blank out the spans where a pipe is legitimate, keeping length irrelevant."""
    line = re.sub(r"\{\{.*?\}\}", "", line)      # Liquid expression
    line = re.sub(r"\{%.*?%\}", "", line)        # Liquid tag
    line = re.sub(r"`[^`]*`", "", line)          # inline code
    line = line.replace("&#124;", "")            # already escaped
    return line


def main() -> int:
    problems = []
    for path in sorted(ROOT.rglob("*.md")):
        # Only files Jekyll actually renders. `_site` is build output, and the
        # dotted dirs (.kiro specs, .github) are notes-to-self that no kramdown
        # ever sees — flagging a pipe there is noise that trains you to ignore
        # the check.
        if "_site" in path.parts or any(p.startswith(".") for p in path.parts):
            continue
        in_fence = False
        for lineno, raw in enumerate(path.read_text().splitlines(), 1):
            line = raw.strip()
            if line.startswith("```") or line.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            # a real table: the row starts with `|`, or it's the delimiter rule
            if line.startswith("|") or re.match(r"^[\s:|-]+$", line) and "|" in line:
                continue
            if "|" in strip_safe(line):
                problems.append((path.relative_to(ROOT), lineno, line[:90]))

    if problems:
        print("BARE `|` IN PROSE — kramdown will render these as a <table>:\n")
        for rel, lineno, text in problems:
            print(f"  {rel}:{lineno}")
            print(f"    {text}")
        print("\nFix: write the pipe as `&#124;` (or wrap the span in backticks if "
              "it's code).")
        return 1
    print("✓ No bare `|` in prose.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
