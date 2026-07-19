# Theory figure (Figure 1)

Figure 1 of the preregistration is generated from a machine-readable theory
specification rather than drawn by hand. The single source of truth is
`intract.theory.yaml`, a [theoryforge](https://github.com/pablobernabeu/theoryforge)
specification of the InTRACt theory: its constructs, the labelled propositions
P1–P6, the pre-registered predictions, the alternative accounts, and the
state-of-the-art findings rendered as the figure's top band.

`generate_theory_svg.py` validates the specification with the theoryforge
package and lays out the banded diagram deterministically, writing
`../mindmap.svg`. The SVG is then rendered with the Chromium that ships with
`puppeteer` (no system image tools required) into two artefacts:

- `../mindmap.png` — a high-DPI raster, used by the repository README;
- `../mindmap.pdf` — a vector PDF embedded in the preregistration PDF, so the
  figure text stays selectable, searchable and indexable.

The preregistration's HTML build inlines `../mindmap.svg` directly, which keeps
the figure text selectable there too.

## Edit and regenerate

1. Edit `intract.theory.yaml`. Never edit the SVG, which is generated.
2. Install the renderer once (downloads a headless Chromium):

   ```sh
   npm install
   ```

3. Regenerate the figure:

   ```sh
   python generate_theory_svg.py
   npm run render
   ```

   `npm run render` runs `node render_svg.js ../mindmap.svg ../mindmap.png 3`
   and then `node render_svg.js ../mindmap.svg ../mindmap.pdf`. For a different
   scale or output path, call the script directly, for example
   `node render_svg.js ../mindmap.svg preview.png 2`.

## Files

- `intract.theory.yaml` — the theory specification (edit this).
- `generate_theory_svg.py` — validates the YAML via theoryforge and writes
  `../mindmap.svg`.
- `render_svg.js` — renders an SVG to PNG (raster) or PDF (vector text) via the
  puppeteer-bundled Chromium.
- `package.json` — declares the single `puppeteer` dependency and the `render`
  script.
