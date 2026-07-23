#!/usr/bin/env python3
"""Validate every internal link on the recipes site resolves to a real page.

Checks two link systems:
  1. index.md HTML anchors:      href="./r/slug"  href="./a/slug"
  2. body-text cross-links:      {{ '/r/slug' | relative_url }}  (r/, a/, drafts/, *.md)

A target is valid if a matching file exists (r/slug.md, steering.html, …) OR a page
declares `permalink: /that/path`. Run from the repo root:  python3 bin/check-links.py

Exits non-zero if any real link is broken. The literal `/r/slug` example inside
changelog.md prose is ignored (it documents the baseurl bug, it's not a link).
"""
import re, glob, os, sys

def build_valid():
    valid = {'/'}
    for f in (glob.glob('r/*.md') + glob.glob('a/*.md') + glob.glob('drafts/*.md')
              + glob.glob('*.md') + glob.glob('*.html')):
        valid.add('/' + f.rsplit('.', 1)[0])          # /r/foo, /steering, /drafts/bar
        pm = re.search(r'^permalink:\s*(\S+)', open(f).read()[:800], re.M)
        if pm:
            valid.add('/' + pm.group(1).strip().strip('/'))
    return valid

def ok(target, valid):
    t = target.split('#')[0].rstrip('/')
    t = '/' + t.lstrip('.').lstrip('/')
    return t == '/' or t in valid

def main():
    valid = build_valid()
    problems = []

    # 1. index.md ./ anchors
    for m in re.findall(r'href="(\./[^"#]+)"', open('index.md').read()):
        if not ok(m, valid):
            problems.append(('index.md', m))

    # 2. relative_url body links
    for f in glob.glob('r/*.md') + glob.glob('a/*.md') + glob.glob('drafts/*.md') + glob.glob('*.md'):
        for m in re.findall(r"\{\{ *'([^']+)' *\| *relative_url *\}\}", open(f).read()):
            if m == '/r/slug' and f == 'changelog.md':   # documented example, not a link
                continue
            if not ok(m, valid):
                problems.append((f, m))

    if problems:
        print("BROKEN INTERNAL LINKS:")
        for f, t in problems:
            print(f"  {f} -> {t}")
        sys.exit(1)
    print("✓ All internal links resolve (files + permalinks).")

if __name__ == '__main__':
    main()
