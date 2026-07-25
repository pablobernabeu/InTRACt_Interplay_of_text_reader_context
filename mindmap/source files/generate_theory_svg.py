"""Generate Figure 1 (mindmap.svg) from the theoryforge theory specification.

Reads intract.theory.yaml (validated through theoryforge), lays out the banded
theory diagram deterministically, and writes ../mindmap.svg. Rasterise with
`npm run render` (render_svg.js), which writes ../mindmap.png (raster) and
../mindmap.pdf (vector).

The layout runs from top to bottom: the established findings the theory builds
on, the constructs and labelled propositions, the pre-registered predictions,
the alternative accounts the analyses weigh against, and the unmeasured account
that bounds interpretation without being tested. Box heights are computed from
wrapped text, so content never overlaps and inner margins stay equal.
"""
import sys

import theoryforge as tf

sys.stdout.reconfigure(encoding="utf-8")

# ---- palette (matched to the theoryforge example figure) -------------------
BAND_BG = "#f5f5f5"
BAND_BORDER = "#e2e2e2"
BAND_LABEL = "#6b6b6b"
BOX_FILL_DARK = "#c9d8ea"
BOX_FILL_LIGHT = "#e8eef6"
BOX_BORDER = "#33567a"
LIT_FILL = "#eef1f5"
LIT_BORDER = "#c8cfd8"
TEXT = "#222222"
CITE = "#6b6b6b"
ARROW = "#33567a"
PRED_FILL = "#faf3e0"
PRED_BORDER = "#cfa93f"
PRED_ID = "#8a6d1a"
TELLS = "#8a6d1a"
ALT_BORDER = "#c9302c"
ALT_LABEL = "#7a1f1c"

W = 950           # canvas width (narrow: the figure is placed at text width, so a
                  # narrower canvas renders every glyph larger on the page; 950 is
                  # the narrowest width that still leaves room on the page for the
                  # APA number line, title line and note alongside the figure)
M = 14            # outer margin
PAD = 12          # inner padding of boxes
GAP = 13          # gap between sibling boxes
FS = 13           # base font size
LH = 16.5         # line height
CW = 0.52         # average character width as a fraction of font size


def wrap(text: str, width_px: float, fs: float = FS) -> list[str]:
    """Greedy wrap by estimated character count. Deterministic."""
    maxc = max(8, int(width_px / (fs * CW)))
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if len(cand) <= maxc:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(s) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("b(", "&#946;("))  # b( -> beta(


class SVG:
    def __init__(self):
        self.parts: list[str] = []

    def rect(self, x, y, w, h, fill, stroke, rx=8, sw=1.2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, fs=FS, fill=TEXT, weight="normal", style="normal",
             anchor="start"):
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" fill="{fill}" '
            f'font-weight="{weight}" font-style="{style}" text-anchor="{anchor}">{esc(s)}</text>')

    def lines(self, x, y, lines_, fs=FS, fill=TEXT, weight="normal", style="normal",
              anchor="start", lh=LH):
        for i, ln in enumerate(lines_):
            self.text(x, y + i * lh, ln, fs, fill, weight, style, anchor)
        return y + len(lines_) * lh

    def arrow(self, x1, y1, x2, y2, label=None, dash=None, label_dy=-5):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{ARROW}" stroke-width="1.4" marker-end="url(#arr)"{d}/>')
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.text(mx, my + label_dy, label, fs=12, fill=ARROW, style="italic",
                      anchor="middle")

    def elbow(self, x1, y1, x2, y2, midx, label=None, dash=None):
        """Horizontal, then vertical, then horizontal arrow through a given elbow x.

        The label sits just after the source, on the side of the first horizontal
        segment that the elbow turns away from, so the vertical segment cannot
        strike through it however long the relation word is.
        """
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<path d="M {x1:.1f} {y1:.1f} L {midx:.1f} {y1:.1f} L {midx:.1f} {y2:.1f} '
            f'L {x2:.1f} {y2:.1f}" fill="none" stroke="{ARROW}" stroke-width="1.4" '
            f'marker-end="url(#arr)"{d}/>')
        if label:
            self.text(x1 + 10, y1 + (14 if y2 < y1 else -6), label, fs=12,
                      fill=ARROW, style="italic")

    def elbow_up(self, x1, y1, x2, y2, label=None, dash=None):
        """Horizontal from the source, then vertical up into the target's bottom edge."""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" '
            f'fill="none" stroke="{ARROW}" stroke-width="1.4" '
            f'marker-end="url(#arr)"{d}/>')
        if label:
            self.text(x1 + 10, y1 - 6, label, fs=12, fill=ARROW, style="italic")


def main() -> None:
    T = tf.read("intract.theory.yaml").data

    svg = SVG()
    y = float(M)  # running vertical cursor; tight top margin (no blank space)

    # ---------------- band 1: established findings the theory builds on -----
    bg = T["background"]
    n = len(bg)
    bw = (W - 2 * M - 2 * PAD - (n - 1) * GAP) / n
    blocks = []
    maxh = 0.0
    for b in bg:
        st = wrap(b["statement"], bw - 2 * PAD, 12.5)
        so = wrap(f"({b['sources']})", bw - 2 * PAD, 11.5)
        h = PAD + len(st) * 16 + 6 + len(so) * 14.5 + PAD - 4
        blocks.append((st, so, h))
        maxh = max(maxh, h)
    band1_h = 26 + PAD + maxh + PAD
    svg.rect(M, y, W - 2 * M, band1_h, BAND_BG, BAND_BORDER, rx=6)
    svg.text(M + PAD, y + 18, "Established findings the theory builds on",
             fs=13, fill=BAND_LABEL, weight="bold")
    by = y + 26 + PAD
    for i, (st, so, h) in enumerate(blocks):
        bx = M + PAD + i * (bw + GAP)
        svg.rect(bx, by, bw, maxh, LIT_FILL, LIT_BORDER, rx=6)
        # centre the content vertically so leftover height splits evenly
        content_h = len(st) * 16 + 6 + len(so) * 14.5
        ty0 = by + (maxh - content_h) / 2 + 10
        ty = svg.lines(bx + PAD, ty0, st, fs=12.5, lh=16)
        svg.lines(bx + PAD, ty + 6, so, fs=11.5, fill=CITE, style="italic", lh=14.5)
    y += band1_h

    # connector
    cx = W / 2
    svg.arrow(cx, y + 4, cx, y + 34)
    svg.text(cx + 8, y + 22, "motivates", fs=12, fill=BAND_LABEL, style="italic")
    y += 40

    # ---------------- band 2: constructs and propositions -------------------
    C = {c["id"]: c for c in T["constructs"]}

    def clabel(cid):
        return C[cid].get("display", C[cid]["label"])

    box_w = 214
    out_w = 190

    def box_h(cid, w):
        return 2 * PAD + len(wrap(clabel(cid), w - 2 * PAD)) * LH - 4

    band2_top = y
    inner_top = band2_top + 26 + PAD + 22  # extra headroom for the dimension tags

    # middle stack, top to bottom: lexdist (P1), syntax (P2), coherence (P3),
    # fluency (P5), so proposition numbers read in order
    mid_x = M + PAD + 300
    stack = ["c_lexdist", "c_syntax", "c_coherence", "c_fluency"]
    sy = inner_top
    mid_pos = {}
    for cid in stack:
        h = box_h(cid, box_w)
        mid_pos[cid] = (mid_x, sy, box_w, h)
        sy += h + 26
    mid_bottom = sy - 26

    def dim_tag(x, yy, label):
        svg.parts.append(
            f'<text x="{x:.1f}" y="{yy:.1f}" font-size="11.5" fill="{ARROW}" '
            f'font-weight="bold" letter-spacing="2.2" opacity="0.75">{esc(label)}</text>')

    # left column: experience aligned with fluency (its target); language below
    left_x = M + PAD + 12
    h_exp = box_h("c_experience", box_w)
    exp_y = mid_pos["c_fluency"][1] + (mid_pos["c_fluency"][3] - h_exp) / 2
    h_lang = box_h("c_language", box_w)
    lang_y = max(exp_y + h_exp, mid_bottom) + 34

    # outcome: right, just tall enough for the four incoming arrows to fan clearly
    out_x = W - M - PAD - out_w - 12
    h_out = max(box_h("c_rt", out_w), 120)
    out_y = (inner_top + mid_bottom) / 2 - h_out / 2

    band2_bottom = max(mid_bottom, lang_y + h_lang, out_y + h_out) + PAD + 10
    band2_h = band2_bottom - band2_top
    svg.rect(M, band2_top, W - 2 * M, band2_h, BAND_BG, BAND_BORDER, rx=6)
    svg.text(M + PAD, band2_top + 18, "The theory: constructs and labelled propositions",
             fs=13, fill=BAND_LABEL, weight="bold")

    def draw_construct(cid, x, yy, w, h, dark=False):
        svg.rect(x, yy, w, h, BOX_FILL_DARK if dark else BOX_FILL_LIGHT, BOX_BORDER,
                 rx=8, sw=1.4)
        ls = wrap(clabel(cid), w - 2 * PAD)
        ty = yy + (h - len(ls) * LH) / 2 + LH - 4
        svg.lines(x + w / 2, ty, ls, weight="bold", anchor="middle")

    for cid in stack:
        x, yy, w, h = mid_pos[cid]
        draw_construct(cid, x, yy, w, h)
    draw_construct("c_experience", left_x, exp_y, box_w, h_exp, dark=True)
    draw_construct("c_language", left_x, lang_y, box_w, h_lang, dark=True)
    draw_construct("c_rt", out_x, out_y, out_w, h_out)

    # InTRACt dimension tags
    dim_tag(mid_x + 2, mid_pos["c_lexdist"][1] - 8, "TEXT")
    dim_tag(left_x + 2, exp_y - 8, "READER")
    dim_tag(left_x + 2, lang_y - 8, "CONTEXT")
    dim_tag(out_x + 2, out_y - 8, "OUTCOME")

    P = {p["id"]: p for p in T["propositions"]}

    # P4: experience -> fluency (same row, straight arrow)
    svg.arrow(left_x + box_w, exp_y + h_exp / 2, mid_x - 6,
              mid_pos["c_fluency"][1] + mid_pos["c_fluency"][3] / 2,
              label=f"P4 {P['p4']['relation']}")
    # P1, P2, P3, P5: middle stack -> outcome; staggered elbows, labels at source
    edges = (("p1", "c_lexdist"), ("p2", "c_syntax"),
             ("p3", "c_coherence"), ("p5", "c_fluency"))
    base_mid = (mid_x + box_w + out_x) / 2
    for i, (pid, cid) in enumerate(edges):
        x, yy, w, h = mid_pos[cid]
        src_y = yy + h / 2
        tgt_y = out_y + 14 + i * (h_out - 28) / (len(edges) - 1)
        svg.elbow(x + w + 4, src_y, out_x - 6, tgt_y, midx=base_mid + 16 * i - 24,
                  label=f"P{pid[1]} {P[pid]['relation']}")
    # P6: language moderates (dashed; up into the outcome box's bottom edge)
    svg.elbow_up(left_x + box_w + 4, lang_y + h_lang / 2, out_x + out_w / 2,
                 out_y + h_out + 6, label=f"P6 {P['p6']['relation']}", dash="5,4")
    y = band2_bottom

    # connector
    svg.arrow(cx, y + 4, cx, y + 34)
    svg.text(cx + 8, y + 22, "entails", fs=12, fill=BAND_LABEL, style="italic")
    y += 40

    # ---------------- band 3: predictions -----------------------------------
    preds = T["predictions"]
    alts = {a["id"]: a["label"] for a in T["alternatives"]}
    n = len(preds)
    pw = (W - 2 * M - 2 * PAD - (n - 1) * GAP) / n
    cards = []
    maxh = 0.0
    for p in preds:
        pid = p["test_label"].split(" - ")[0]
        tag = p["test_label"].split(" - ", 1)[1].strip()
        tag = tag[0].upper() + tag[1:]
        body = wrap(p.get("display", p["statement"]), pw - 2 * PAD, 12)
        tells = "weighed against " + " and ".join(alts[a].lower() for a in p["diagnostic_vs"])
        tl = wrap(tells, pw - 2 * PAD, 11.5)
        tg = wrap(tag, pw - 2 * PAD, 11.5)
        h = PAD + 18 + len(body) * 15.5 + 6 + len(tl) * 14.5 + 6 + len(tg) * 14.5 + PAD - 2
        cards.append((pid, body, tl, tg, h))
        maxh = max(maxh, h)
    band3_h = 26 + PAD + maxh + PAD
    svg.rect(M, y, W - 2 * M, band3_h, BAND_BG, BAND_BORDER, rx=6)
    svg.text(M + PAD, y + 18,
             "Predictions, each pre-registered and tested in the confirmatory analysis",
             fs=13, fill=BAND_LABEL, weight="bold")
    py = y + 26 + PAD
    for i, (pid, body, tl, tg, h) in enumerate(cards):
        px = M + PAD + i * (pw + GAP)
        svg.rect(px, py, pw, maxh, PRED_FILL, PRED_BORDER, rx=6)
        svg.text(px + PAD, py + PAD + 7, pid, fs=13.5, fill=PRED_ID, weight="bold")
        # centre the body + tells-against block between the header and the tag,
        # so leftover height splits evenly rather than pooling in the middle
        block_h = len(body) * 15.5 + 4 + len(tl) * 14.5
        avail_top = py + PAD + 20
        avail_bottom = py + maxh - PAD - len(tg) * 14.5 - 4
        ty0 = avail_top + max(0.0, (avail_bottom - avail_top - block_h) / 2) + 9
        ty = svg.lines(px + PAD, ty0, body, fs=12, lh=15.5)
        ty = svg.lines(px + PAD, ty + 4, tl, fs=11.5, fill=TELLS, style="italic", lh=14.5)
        svg.lines(px + pw - PAD, py + maxh - PAD - (len(tg) - 1) * 14.5 - 2, tg,
                  fs=11.5, weight="bold", anchor="end", lh=14.5)
    y += band3_h + 14

    # ---------------- band 4: alternative accounts ---------------------------
    # Two strips. An alternative that a prediction is pointed at is weighed by
    # the confirmatory analyses; one that no prediction can bear on only bounds
    # the interpretation, and is drawn dashed and captioned as such.
    def alt_strip(top, label, items, dash=None):
        strip_h = 44
        svg.rect(M, top, W - 2 * M, strip_h, "#ffffff", ALT_BORDER, rx=10,
                 sw=1.2, dash=dash)
        svg.text(M + PAD + 6, top + 27, label, fs=13, fill=ALT_LABEL,
                 weight="bold")
        px = M + PAD + 6 + len(label) * 13 * CW + 24
        for a in items:
            t = a["label"]
            wpix = len(t) * 12 * CW + 26
            svg.rect(px, top + 9, wpix, 26, "#ffffff", ALT_BORDER, rx=13,
                     sw=1.1, dash=dash)
            svg.text(px + wpix / 2, top + 27, t, fs=12, anchor="middle")
            px += wpix + 14
        return top + strip_h

    targeted = {a for p in preds for a in p.get("diagnostic_vs", [])}
    y = alt_strip(y, "Alternative accounts weighed by the same tests:",
                  [a for a in T["alternatives"] if a["id"] in targeted])
    untested = [a for a in T["alternatives"] if a["id"] not in targeted]
    if untested:
        y = alt_strip(y + 10, "Unmeasured account, bounds interpretation:",
                      untested, dash="5,4")
    y += M

    height = y
    # Single-line output: the manuscript's HTML build inlines this file as raw
    # HTML, and a one-line element passes through pandoc's raw-HTML parsing
    # verbatim (multi-line SVG gets its root tag stripped).
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height:.0f}" '
        f'font-family="Helvetica, Arial, sans-serif" role="img" '
        f'aria-label="Theoretical scope of the InTRACt study">'
        '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{ARROW}"/></marker></defs>'
        f'<rect x="0" y="0" width="{W}" height="{height:.0f}" fill="#ffffff"/>'
        + " ".join(svg.parts) + "</svg>\n"
    )
    with open("../mindmap.svg", "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"wrote ../mindmap.svg ({W} x {height:.0f})")


if __name__ == "__main__":
    main()
