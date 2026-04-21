---
title: "Risograph Printing and Risograph Color"
category: articles
---

A risograph is a stencil-based digital duplicator made by Riso Kagaku Corporation, a Japanese company founded in 1946 by Noboru Hayama. "Riso" means "ideal" in Japanese. The first Risograph machine was released in 1980, designed for high-volume office printing — schools, churches, community centers. It was never meant for art.

Artists found it anyway.

## How It Works

A risograph prints one color at a time. For each color layer, the machine burns tiny holes into a paper master (the stencil) using thermal technology. The master wraps around a drum filled with ink. As paper feeds through, the drum pushes ink through the stencil holes and onto the sheet.

For a two-color print, you run the paper through twice — once per drum. Three colors, three passes. Each pass introduces slight misregistration: the paper shifts a fraction of a millimeter, so layers don't align perfectly. This is a feature, not a bug.

## The Ink

Risograph inks are soy-based (or rice bran oil-based), not petroleum-based. They're semi-transparent, which means overlapping two colors produces a third. Blue over yellow gives green. Pink over blue gives purple. The transparency is what makes overprinting possible and what gives riso prints their characteristic layered depth.

The inks never fully dry. They absorb into uncoated paper rather than sitting on top of it, which is why riso can only print on uncoated stock. Touch a fresh print and it will smudge slightly. This is permanent — riso prints will always have a faint tactile quality.

## The Color Palette

Riso doesn't use CMYK. Instead, it uses spot colors — each drum holds one specific ink color. There are roughly 50+ ink colors available, though most print shops stock 8–15. Common colors include:

<table class="riso-swatches">
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#0078bf;vertical-align:middle;margin-right:0.4em;"></span>Blue</td><td><code>#0078bf</code></td><td>The workhorse. Deep, slightly cyan-leaning.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#ff48b0;vertical-align:middle;margin-right:0.4em;"></span>Fluorescent Pink</td><td><code>#ff48b0</code></td><td>The signature riso color. Neon, electric, unmistakable.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#f65058;vertical-align:middle;margin-right:0.4em;"></span>Scarlet</td><td><code>#f65058</code></td><td>Warm, slightly orange. Not fire-engine red.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#ff6c2f;vertical-align:middle;margin-right:0.4em;"></span>Orange</td><td><code>#ff6c2f</code></td><td>Pumpkin. Warm and saturated.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#ffb511;vertical-align:middle;margin-right:0.4em;"></span>Sunflower</td><td><code>#ffb511</code></td><td>Bright, clean. Overprints well with blue and red.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#00a95c;vertical-align:middle;margin-right:0.4em;"></span>Green</td><td><code>#00a95c</code></td><td>Grass green, slightly warm.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#009da5;vertical-align:middle;margin-right:0.4em;"></span>Light Teal</td><td><code>#009da5</code></td><td>Blue-green, darker than you'd expect.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#9d7ad2;vertical-align:middle;margin-right:0.4em;"></span>Violet</td><td><code>#9d7ad2</code></td><td>Muted, not violet. More grape than lavender.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#435060;vertical-align:middle;margin-right:0.4em;"></span>Midnight</td><td><code>#435060</code></td><td>Blue-tinted dark grey.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#5ec8e5;vertical-align:middle;margin-right:0.4em;"></span>Aqua</td><td><code>#5ec8e5</code></td><td>Light, airy. Needs dark text.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#ff7477;vertical-align:middle;margin-right:0.4em;"></span>Fluorescent Orange</td><td><code>#ff7477</code></td><td>Coral-leaning. Glows under certain light.</td></tr>
<tr><td><span style="display:inline-block;width:0.9em;height:0.9em;background:#bb8b41;vertical-align:middle;margin-right:0.4em;"></span>Metallic Gold</td><td><code>#bb8b41</code></td><td>Actual metallic sheen on paper.</td></tr>
</table>

Hex values are approximations — riso inks don't conform to any digital color standard. They look different on different papers, at different ink densities, and under different lighting. The hex codes from [Stencil Wiki](https://stencil.wiki/colors) and the [riso-colors npm package](https://www.npmjs.com/package/riso-colors) are the closest community-maintained references.

## Overprinting

Because the inks are transparent, layering two colors creates a third. This is the core creative technique in risography. A two-color print (say, blue and fluorescent pink) actually gives you three colors: blue, pink, and the dark magenta where they overlap.

Designers working with riso think in layers, not in final colors. You separate your artwork into individual color channels — one grayscale image per ink color — and the machine prints them sequentially. Where the layers overlap, the inks mix optically and physically on the paper.

This is fundamentally different from CMYK printing, where four inks are applied in precise halftone dots to simulate continuous color. Riso overprinting is coarser, more visible, and more unpredictable. That's the appeal.

## Why It Looks the Way It Looks

Several mechanical properties combine to create the riso aesthetic:

**Misregistration.** Each pass through the machine shifts the paper slightly. Layers don't align perfectly. This creates the characteristic "offset" look where colors bleed past their intended boundaries.

**Grain and texture.** The stencil process produces a visible dot pattern, especially in midtones. Solid areas have slight variation in ink density. Nothing is perfectly flat.

**Ink absorption.** Because the ink soaks into the paper rather than sitting on top, colors appear slightly muted compared to their digital hex values. The paper color (usually off-white or cream) shows through.

**Limited palette.** Working with 2–3 spot colors forces graphic simplicity. You can't reach for a gradient or a subtle tonal shift. You work with flat color, overprint, and halftone.

## Riso Color in Digital Design

The riso aesthetic has migrated from print to screen. Designers use riso-inspired palettes in web design, illustration, and branding because the colors have a specific character: saturated but not neon, vibrant but not digital-feeling, limited but expressive.

When translating riso colors to digital, a few principles apply:

**Avoid pure primaries.** `#ff0000` is not a riso red. Riso colors are always slightly shifted — warmer, cooler, or more muted than their pure hex equivalents. The red is more brick than fire engine. The blue leans cyan, not cobalt.

**Keep saturation high but not maxed.** Riso inks are vivid, but they're printed on absorbent paper, which softens them. In digital, this translates to colors around 60–80% saturation, not 100%.

**Limit your palette.** A riso print rarely uses more than 3–4 colors. The constraint is what makes the aesthetic work. In digital, this means picking 2–3 accent colors and a neutral, not a rainbow.

**Think about overprint.** If two of your colors would overlap in a print, what color would they make? Good riso palettes produce pleasing overprint combinations. Blue + yellow = green. Pink + blue = purple. If your palette's overlaps produce mud, reconsider.

## Sources

Content was rephrased for compliance with licensing restrictions.

- [Stencil Wiki — Risograph Color Chart](https://stencil.wiki/colors) — community-maintained ink color reference with hex values
- [riso-colors on npm](https://www.npmjs.com/package/riso-colors) — JSON dataset of riso ink colors with hex, Pantone, and Z-Type codes
- [Secret Riso Club — Riso Basics](https://secretrisoclub.com/RISO-BASICS) — overview of the printing process
- [Athletics NYC — Process Spotlight: Risograph Printing](https://athleticsnyc.com/news/process-spotlight-risograph-printing) — history and technique
- [Nothing Major — Rise of the Risograph](http://nothingmajor.com/features/17-rise-of-the-risograph-part-one/) — history of Riso Kagaku and the art printing movement
- [Martian Press — Ink Colors](https://martian.press/ink-colors) — riso ink swatches with hex and Pantone codes
