---
name: risograph-colors
description: Guide for picking risograph-inspired colors. Use when designing color palettes that feel vibrant, printed, and slightly handmade.
triggers:
  - "risograph colors"
  - "riso palette"
  - "pick colors"
  - "color palette"
---

# Risograph Color Palettes

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" in this document are to be interpreted as described in RFC 2119.

## Background

Risograph (riso) printing uses soy-based inks applied one color at a time through stencils. The inks have a specific character:

- Slightly less saturated than pure digital primaries
- Vibrant but not neon — "saturated but not fluorescent"
- Slight transparency and grain when printed
- Limited palette per print (typically 2–4 colors)

Digital palettes inspired by riso capture this "vibrant but handmade" feel without being cartoonish or neon.

## Color Selection Rules

- Colors MUST be saturated but not pure primaries. Use hex values around 60–80% saturation, not 100%.
- Lightness SHOULD be in the 40–55% range. Too dark reads as muddy; too light loses presence.
- Avoid pure hex values like `#ff0000`, `#0000ff`, `#00ff00` — they feel digital, not printed.
- Each color MUST have enough perceptual distance from the others to be distinguishable at a glance.
- When pairing with white text, the color MUST achieve at least 4.5:1 contrast (WCAG AA).

## Canonical Riso Palette (good starting point)

| Role | Hex | Riso Ink Name |
|---|---|---|
| Red | `#f65058` | Scarlet |
| Orange | `#ff6c2f` | Orange |
| Green | `#00a95c` | Green |
| Pink | `#ff48b0` | Fluorescent Pink |
| Teal | `#009da5` | Light Teal |
| Violet | `#9d7ad2` | Violet |
| Dark Grey | `#435060` | Midnight |
| Blue | `#0078bf` | Blue |

## How to Pick a Custom Riso Palette

1. Start with a hue wheel. Space your hues evenly if you want a balanced palette.
2. Set all hues to the same HSL lightness (around 45%) and saturation (around 70%).
3. Adjust individually:
   - Yellow and orange naturally read as lighter — darken them slightly
   - Blue and purple naturally read as darker — lighten them slightly
4. Test every color against white text. If contrast fails, go darker, not more saturated.
5. Always include at least one neutral (dark grey, not black) as a grounding color.

## What to Avoid

- Pure digital primaries (`#ff0000`, `#00ff00`, `#0000ff`) — too harsh, feels like a default OS color picker
- Muted/pastel colors — loses the "printed" energy
- Fluorescent highlighter yellow — poor white-text contrast, feels dated
- More than 7 colors in a single palette — loses distinctness

## References

- [Stencil.wiki — Risograph Color Chart](https://stencil.wiki/colors) — actual riso ink colors
- [Risograph Inks List](https://www.riso.co.jp/english/brochure/catalog/color.pdf) — official RISO ink swatches
