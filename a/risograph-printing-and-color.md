---
title: Risograph Printing and Color
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

Riso doesn't use CMYK. Instead, it uses spot colors — each drum holds one specific ink color. There are 77 documented ink colors, though most print shops stock 8–15. The full catalog, sourced from the [riso-colors npm package](https://www.npmjs.com/package/riso-colors) and [Stencil Wiki](https://stencil.wiki/colors):

**Reds & Pinks**

<table class="riso-swatches">
<tr><td>Scarlet</td><td><span class="pill-sample" style="background:#f65058">#f65058</span></td><td>Warm, slightly orange. Not fire-engine red.</td></tr>
<tr><td>Bright Red</td><td><span class="pill-sample" style="background:#f15060">#f15060</span></td><td>Close to Scarlet, slightly cooler.</td></tr>
<tr><td>Red</td><td><span class="pill-sample" style="background:#ff665e">#ff665e</span></td><td>Warm red, coral-leaning.</td></tr>
<tr><td>Crimson</td><td><span class="pill-sample" style="background:#e45d50">#e45d50</span></td><td>Earthy, brick-adjacent.</td></tr>
<tr><td>Marine Red</td><td><span class="pill-sample" style="background:#d2515e">#d2515e</span></td><td>Muted, dusty red.</td></tr>
<tr><td>Tomato</td><td><span class="pill-sample" style="background:#d2515e">#d2515e</span></td><td>Same hex as Marine Red.</td></tr>
<tr><td>Brick</td><td><span class="pill-sample" style="background:#a75154">#a75154</span></td><td>Dark, earthy.</td></tr>
<tr><td>Cranberry</td><td><span class="pill-sample" style="background:#d1517a">#d1517a</span></td><td>Pink-red, berry tone.</td></tr>
<tr><td>Raspberry Red</td><td><span class="pill-sample" style="background:#d1517a">#d1517a</span></td><td>Same hex as Cranberry.</td></tr>
<tr><td>Maroon</td><td><span class="pill-sample" style="background:#9e4c6e">#9e4c6e</span></td><td>Deep plum-red.</td></tr>
<tr><td>Burgundy</td><td><span class="pill-sample" style="background:#914e72">#914e72</span></td><td>Wine-dark.</td></tr>
<tr><td>Wine</td><td><span class="pill-sample" style="background:#914e72">#914e72</span></td><td>Same hex as Burgundy.</td></tr>
<tr><td>Fluorescent Pink</td><td><span class="pill-sample" style="background:#ff48b0">#ff48b0</span></td><td>The signature riso color. Neon, electric.</td></tr>
<tr><td>Fluorescent Red</td><td><span class="pill-sample" style="background:#ff4c65">#ff4c65</span></td><td>Neon red-pink.</td></tr>
<tr><td>Fluorescent Orange</td><td><span class="pill-sample" style="background:#ff7477">#ff7477</span></td><td>Coral-leaning. Glows under certain light.</td></tr>
<tr><td>Bubble Gum</td><td><span class="pill-sample" style="background:#f984ca">#f984ca</span></td><td>Bright candy pink.</td></tr>
<tr><td>Light Mauve</td><td><span class="pill-sample" style="background:#e6b5c9">#e6b5c9</span></td><td>Pale dusty pink.</td></tr>
<tr><td>Dark Mauve</td><td><span class="pill-sample" style="background:#bd8ca6">#bd8ca6</span></td><td>Muted rose.</td></tr>
<tr><td>Bisque</td><td><span class="pill-sample" style="background:#f2cdcf">#f2cdcf</span></td><td>Near-white blush.</td></tr>
<tr><td>Coral</td><td><span class="pill-sample" style="background:#ff8e91">#ff8e91</span></td><td>Soft salmon-pink.</td></tr>
</table>

**Oranges & Yellows**

<table class="riso-swatches">
<tr><td>Orange</td><td><span class="pill-sample" style="background:#ff6c2f">#ff6c2f</span></td><td>Pumpkin. Warm and saturated.</td></tr>
<tr><td>Pumpkin</td><td><span class="pill-sample" style="background:#ff6f4c">#ff6f4c</span></td><td>Slightly lighter than Orange.</td></tr>
<tr><td>Paprika</td><td><span class="pill-sample" style="background:#ee7f4b">#ee7f4b</span></td><td>Warm spice tone.</td></tr>
<tr><td>Apricot</td><td><span class="pill-sample" style="background:#f6a04d">#f6a04d</span></td><td>Soft, warm peach-orange.</td></tr>
<tr><td>Melon</td><td><span class="pill-sample" style="background:#ffae3b">#ffae3b</span></td><td>Golden amber.</td></tr>
<tr><td>Sunflower</td><td><span class="pill-sample" style="background:#ffb511">#ffb511</span></td><td>Bright, clean. Overprints well with blue.</td></tr>
<tr><td>Yellow</td><td><span class="pill-sample" style="background:#ffe800">#ffe800</span></td><td>Pure, vivid yellow.</td></tr>
<tr><td>Fluorescent Yellow</td><td><span class="pill-sample" style="background:#ffe900">#ffe900</span></td><td>Neon yellow. Nearly identical to Yellow.</td></tr>
<tr><td>Light Lime</td><td><span class="pill-sample" style="background:#e3ed55">#e3ed55</span></td><td>Yellow-green, chartreuse.</td></tr>
<tr><td>Bright Olive Green</td><td><span class="pill-sample" style="background:#b49f29">#b49f29</span></td><td>Dark olive-gold.</td></tr>
</table>

**Golds & Browns**

<table class="riso-swatches">
<tr><td>Flat Gold</td><td><span class="pill-sample" style="background:#bb8b41">#bb8b41</span></td><td>Matte gold, no metallic sheen.</td></tr>
<tr><td>Bright Gold</td><td><span class="pill-sample" style="background:#ba8032">#ba8032</span></td><td>Warmer, deeper gold.</td></tr>
<tr><td>Metallic Gold</td><td><span class="pill-sample" style="background:#ac936e">#ac936e</span></td><td>Actual metallic sheen on paper.</td></tr>
<tr><td>Copper</td><td><span class="pill-sample" style="background:#bd6439">#bd6439</span></td><td>Warm metallic brown.</td></tr>
<tr><td>Brown</td><td><span class="pill-sample" style="background:#925f52">#925f52</span></td><td>Warm, earthy.</td></tr>
<tr><td>Mahogany</td><td><span class="pill-sample" style="background:#8e595a">#8e595a</span></td><td>Dark reddish-brown.</td></tr>
</table>

**Greens**

<table class="riso-swatches">
<tr><td>Fluorescent Green</td><td><span class="pill-sample" style="background:#44d62c">#44d62c</span></td><td>Neon, electric green.</td></tr>
<tr><td>Kelly Green</td><td><span class="pill-sample" style="background:#67b346">#67b346</span></td><td>Classic bright green.</td></tr>
<tr><td>Green</td><td><span class="pill-sample" style="background:#00a95c">#00a95c</span></td><td>Grass green, slightly warm.</td></tr>
<tr><td>Emerald</td><td><span class="pill-sample" style="background:#19975d">#19975d</span></td><td>Rich jewel green.</td></tr>
<tr><td>Ivy</td><td><span class="pill-sample" style="background:#169b62">#169b62</span></td><td>Deep, saturated green.</td></tr>
<tr><td>Grass</td><td><span class="pill-sample" style="background:#397e58">#397e58</span></td><td>Dark, muted lawn green.</td></tr>
<tr><td>Forest</td><td><span class="pill-sample" style="background:#516e5a">#516e5a</span></td><td>Dark, desaturated.</td></tr>
<tr><td>Spruce</td><td><span class="pill-sample" style="background:#4a635d">#4a635d</span></td><td>Blue-green, very dark.</td></tr>
<tr><td>Moss</td><td><span class="pill-sample" style="background:#68724d">#68724d</span></td><td>Olive-green, earthy.</td></tr>
<tr><td>Slate</td><td><span class="pill-sample" style="background:#5e695e">#5e695e</span></td><td>Gray-green.</td></tr>
<tr><td>Hunter Green</td><td><span class="pill-sample" style="background:#407060">#407060</span></td><td>Classic dark green.</td></tr>
</table>

**Teals & Aquas**

<table class="riso-swatches">
<tr><td>Sea Foam</td><td><span class="pill-sample" style="background:#62c2b1">#62c2b1</span></td><td>Light, minty.</td></tr>
<tr><td>Mint</td><td><span class="pill-sample" style="background:#82d8d5">#82d8d5</span></td><td>Pale, airy teal.</td></tr>
<tr><td>Turquoise</td><td><span class="pill-sample" style="background:#00aa93">#00aa93</span></td><td>Vivid blue-green.</td></tr>
<tr><td>Light Teal</td><td><span class="pill-sample" style="background:#009da5">#009da5</span></td><td>Blue-green, darker than you'd expect.</td></tr>
<tr><td>Teal</td><td><span class="pill-sample" style="background:#00838a">#00838a</span></td><td>Deep, classic teal.</td></tr>
<tr><td>Pine</td><td><span class="pill-sample" style="background:#237e74">#237e74</span></td><td>Dark teal-green.</td></tr>
<tr><td>Lagoon</td><td><span class="pill-sample" style="background:#2f6165">#2f6165</span></td><td>Very dark teal.</td></tr>
<tr><td>Smoky Teal</td><td><span class="pill-sample" style="background:#5f8289">#5f8289</span></td><td>Muted, gray-teal.</td></tr>
<tr><td>Aqua</td><td><span class="pill-sample" style="background:#5ec8e5">#5ec8e5</span></td><td>Light, airy. Needs dark text.</td></tr>
<tr><td>Mist</td><td><span class="pill-sample" style="background:#d5e4c0">#d5e4c0</span></td><td>Pale sage-green. Nearly white.</td></tr>
</table>

**Blues**

<table class="riso-swatches">
<tr><td>Cornflower</td><td><span class="pill-sample" style="background:#62a8e5">#62a8e5</span></td><td>Light, friendly blue.</td></tr>
<tr><td>Sky Blue</td><td><span class="pill-sample" style="background:#4982cf">#4982cf</span></td><td>Medium, slightly muted.</td></tr>
<tr><td>Blue</td><td><span class="pill-sample" style="background:#0078bf">#0078bf</span></td><td>The workhorse. Deep, slightly cyan-leaning.</td></tr>
<tr><td>Sea Blue</td><td><span class="pill-sample" style="background:#0074a2">#0074a2</span></td><td>Darker, greener blue.</td></tr>
<tr><td>Lake</td><td><span class="pill-sample" style="background:#235ba8">#235ba8</span></td><td>Deep, rich blue.</td></tr>
<tr><td>Medium Blue</td><td><span class="pill-sample" style="background:#3255a4">#3255a4</span></td><td>Classic mid-blue.</td></tr>
<tr><td>RisoFederal Blue</td><td><span class="pill-sample" style="background:#3d5588">#3d5588</span></td><td>Muted navy.</td></tr>
<tr><td>Steel</td><td><span class="pill-sample" style="background:#375e77">#375e77</span></td><td>Blue-gray, industrial.</td></tr>
<tr><td>Indigo</td><td><span class="pill-sample" style="background:#484d7a">#484d7a</span></td><td>Dark blue-purple.</td></tr>
<tr><td>Midnight</td><td><span class="pill-sample" style="background:#435060">#435060</span></td><td>Blue-tinted dark grey.</td></tr>
</table>

**Purples**

<table class="riso-swatches">
<tr><td>Violet</td><td><span class="pill-sample" style="background:#9d7ad2">#9d7ad2</span></td><td>Muted, more grape than lavender.</td></tr>
<tr><td>Orchid</td><td><span class="pill-sample" style="background:#aa60bf">#aa60bf</span></td><td>Bright, warm purple.</td></tr>
<tr><td>Purple</td><td><span class="pill-sample" style="background:#765ba7">#765ba7</span></td><td>Classic mid-purple.</td></tr>
<tr><td>Plum</td><td><span class="pill-sample" style="background:#845991">#845991</span></td><td>Dark, warm purple.</td></tr>
<tr><td>Raisin</td><td><span class="pill-sample" style="background:#775d7a">#775d7a</span></td><td>Muted, dusty purple.</td></tr>
<tr><td>Grape</td><td><span class="pill-sample" style="background:#6c5d80">#6c5d80</span></td><td>Dark, desaturated.</td></tr>
</table>

**Neutrals**

<table class="riso-swatches">
<tr><td>Black</td><td><span class="pill-sample" style="background:#000000">#000000</span></td><td>True black.</td></tr>
<tr><td>Charcoal</td><td><span class="pill-sample" style="background:#70747c">#70747c</span></td><td>Dark neutral gray.</td></tr>
<tr><td>Light Gray</td><td><span class="pill-sample" style="background:#88898a">#88898a</span></td><td>Mid gray.</td></tr>
<tr><td>Gray</td><td><span class="pill-sample" style="background:#928d88">#928d88</span></td><td>Warm gray.</td></tr>
<tr><td>Granite</td><td><span class="pill-sample" style="background:#a5aaa8">#a5aaa8</span></td><td>Cool, light gray.</td></tr>
<tr><td>White</td><td><span class="pill-sample" style="background:#ffffff;color:#888;border:1px solid #ddd">#ffffff</span></td><td>Opaque white ink.</td></tr>
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
