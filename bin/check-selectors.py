#!/usr/bin/env python3
"""Catch selectors that GitHub Pages' Sass silently deletes.

WHY THIS EXISTS. Pages builds this site with jekyll-sass-converter 1.5.2 -> Ruby
Sass 3.7.4, which predates `:has()`. Standalone, it passes an unknown selector
through untouched. But the moment it has to REBUILD a selector -- nesting the rule
inside a parent block, or using `&` -- it re-parses, fails on `:has` inside
`:not`, and emits the rule with the whole `:not(...)` **dropped**. No warning,
exit 0, green build.

That shipped a real bug: the no-Analysis notes rule went live as an unconditional
`> #steps ~ .notes`, which ties on specificity with `> #analysis ~ .notes` and
wins on source order, so all 70 recipes WITH an Analysis got the wrong band and
the notes text printed on top of the "analysis" head. It compiled clean under
Dart Sass locally and clean on Pages.

WHAT THIS CHECKS. Every `:not(:has(...))` in the stylesheet must appear at the top
level of its block (or be interpolated from a variable, which is textual and never
re-parsed) -- never nested under a parent selector. Run it before pushing a
stylesheet change.

For a definitive check, compile with the same compiler Pages uses:

    gem install --user-install sass -v 3.7.4 --no-document --ignore-dependencies
    ruby -e 'require "sass"
             src = File.read("assets/main.scss").sub(/\\A---\\s*\\n(.*?\\n)?---\\s*\\n/m, "")
             puts Sass::Engine.new(src, syntax: :scss, style: :compressed, cache: false).render' > /tmp/ruby.css
    grep -c ":not(:has" /tmp/ruby.css   # must equal the source count
"""
import re
import sys
from pathlib import Path

SCSS = Path(__file__).resolve().parent.parent / "assets" / "main.scss"

# A `:not(:has(` that Ruby Sass will re-parse and mangle. Interpolated ones
# (`#{$var} > ...`) are safe because interpolation is substituted, not parsed.
FRAGILE = ":not(:has("


def main() -> int:
    src = SCSS.read_text()
    src = re.sub(r"\A---\s*\n(.*?\n)?---\s*\n", "", src, flags=re.S)

    depth = 0                 # brace nesting depth
    at_rule_depth = set()      # depths opened by @media/@supports (not selectors)
    problems = []
    total = 0

    for lineno, raw in enumerate(src.splitlines(), start=1):
        line = re.sub(r"//.*$", "", raw)

        if FRAGILE in line:
            total += line.count(FRAGILE)
            # Nesting depth that comes from SELECTOR blocks only. An @media block
            # does not cause a re-parse; a parent selector does.
            selector_depth = depth - len(at_rule_depth & set(range(depth + 1)))
            interpolated = "#{" in line
            if selector_depth > 0 and not interpolated:
                problems.append((lineno, selector_depth, raw.strip()))

        for ch in line:
            if ch == "{":
                depth += 1
                if re.search(r"@(media|supports|include|each|for|if|else)\b", line):
                    at_rule_depth.add(depth)
            elif ch == "}":
                at_rule_depth.discard(depth)
                depth = max(0, depth - 1)

    print(f"{SCSS.name}: {total} `:not(:has(...))` selector(s)")
    if not problems:
        print("OK — all of them are at the top level of their block "
              "(or interpolated), so Ruby Sass will not strip them.")
        return 0

    print(f"\nFAIL — {len(problems)} nested under a parent selector. Ruby Sass on "
          f"GitHub Pages will DELETE the `:not(...)` and the rule will match "
          f"everything:\n")
    for lineno, d, text in problems:
        print(f"  {SCSS.name}:{lineno} (nested {d} selector level(s) deep)")
        print(f"    {text}")
    print("\nFix: write the full selector out at the top level of its media block, "
          "or build it with an interpolated string variable. `&` does not help — "
          "it re-parses too.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
