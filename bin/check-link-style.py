#!/usr/bin/env python3
"""Flag internal links written as a plain path instead of `relative_url`.

`bin/check-links.py` validates that a link's *target* exists. It cannot see this
class at all: a `./` or `/` path resolves against the page's own URL, so whether
it 404s depends on the permalink's trailing slash, not on the target.

Both shapes have shipped live 404s:
  steering.md   `[Source Name](url)`        -> /recipes/steering/url   (permalink has a slash)
  changelog.md  `[…](./r/matcha-shortbread)` -> /recipes/changelog/r/… (same cause, fixed 2026-08)

Exemptions, both deliberate:
  - index.md's `./` anchors — the homepage is served at `/recipes/`, so `./x`
    resolves under the baseurl. steering.md grants this; all 163 verified 200.
  - anything inside a code span or fence — those document the rule, not links.

Run from the repo root:  python3 bin/check-link-style.py
"""
import re, glob, sys

FENCE = re.compile(r'^```.*?^```', re.M | re.S)
CODE_SPAN = re.compile(r'`[^`\n]*`')
MD_LINK = re.compile(r'\][ ]?\(\s*([^)\s]+)')
HTML_HREF = re.compile(r'href="([^"]+)"')
SKIP_PREFIX = ('http://', 'https://', 'mailto:', '#', '{{', '{%')


def pages():
    """Only files Jekyll renders — a page needs front matter."""
    for f in sorted(set(glob.glob('r/*.md') + glob.glob('a/*.md')
                        + glob.glob('drafts/*.md') + glob.glob('*.md')
                        + glob.glob('*.html'))):
        src = open(f, encoding='utf-8').read()
        if src.startswith('---'):
            yield f, src


def main():
    problems = []
    for f, src in pages():
        prose = CODE_SPAN.sub('`code`', FENCE.sub('', src))
        for target in MD_LINK.findall(prose) + HTML_HREF.findall(prose):
            if target.startswith(SKIP_PREFIX):
                continue
            if f == 'index.md' and target.startswith('./'):
                continue
            problems.append((f, target))

    if problems:
        print("INTERNAL LINKS NOT USING relative_url:")
        for f, t in problems:
            print(f"  {f} -> {t}")
        print("\nWrite  [Text]({{ '/r/slug' | relative_url }})  instead.")
        sys.exit(1)
    print("✓ All internal links use relative_url (or a granted exemption).")


if __name__ == '__main__':
    main()
