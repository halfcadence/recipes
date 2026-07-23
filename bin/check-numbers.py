#!/usr/bin/env python3
"""Validate the recipe `number:` sequence in r/.

Recipe numbers are the sequential chronological IDs shown as the hero superscript
(e.g. gyoza 063). They MUST be: present on every r/ page, unique, and a contiguous
run 1..N with no gaps (N = the recipe count). A gap or duplicate is a silent bug —
the next `number` gets mis-assigned, or two recipes collide. Run from the repo root:

    python3 bin/check-numbers.py

Exits non-zero on any missing field, duplicate, gap, or non-1-based start.
Drafts (drafts/) intentionally have NO number and are not checked.
"""
import re, glob, sys

def main():
    files = sorted(glob.glob('r/*.md'))
    if not files:
        print("No r/*.md files found — run this from the repo root.")
        sys.exit(1)

    nums = {}          # number -> [files]
    missing = []
    for f in files:
        m = re.search(r'^number:\s*(\d+)\s*$', open(f).read(), re.M)
        if not m:
            missing.append(f)
            continue
        nums.setdefault(int(m.group(1)), []).append(f)

    problems = []
    if missing:
        problems.append(f"{len(missing)} r/ page(s) missing a `number:` field:")
        problems += [f"    {f}" for f in missing]

    dupes = {n: fs for n, fs in nums.items() if len(fs) > 1}
    if dupes:
        problems.append("duplicate numbers:")
        for n, fs in sorted(dupes.items()):
            problems.append(f"    {n:>3}: {', '.join(fs)}")

    if nums:
        have = set(nums)
        hi = max(have)
        gaps = sorted(set(range(1, hi + 1)) - have)
        if gaps:
            problems.append(f"gaps in 1..{hi}: {', '.join(map(str, gaps))}")
        if 1 not in have:
            problems.append(f"sequence does not start at 1 (lowest is {min(have)})")

    if problems:
        print("RECIPE NUMBER PROBLEMS:")
        for p in problems:
            print(f"  {p}")
        sys.exit(1)

    hi = max(nums)
    print(f"✓ Recipe numbers OK: contiguous 1..{hi}, {len(nums)} recipes, no gaps or duplicates. Next: {hi + 1}.")

if __name__ == '__main__':
    main()
