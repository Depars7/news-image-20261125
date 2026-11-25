#!/usr/bin/env python3
"""Draw the front page of THE WORLD DISPATCH — Wednesday, 25 November 2026.

Pure Pillow, no network, no randomness, no timestamps: the same input files
always produce the same image.png. Run:  python3 draw_frontpage.py

Layout (1024x1024, margin 28, 6 columns, gutter 12, baseline 8):
  ticker strip -> masthead -> double rule -> red BREAKING banner
  hero image (cols 1-4) + "AROUND THE WORLD" sidebar (cols 5-6)
  lead kicker / headline / deck under the hero
  lower band: 3 story modules x 2 columns (small image + headline + deck)
  footer markets ticker

Type discipline (ui-ux-pro-max: hierarchy first, contrast, no tiny text):
  no meaningful text below 12px; headlines >= 18px; lead + date survive a
  50% downscale. Every text block is measured at render time and the script
  raises if anything overflows its box — a layout bug must fail loudly here,
  never ship as a smear on the page.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
M = 28
PAPER = (244, 239, 230)
INK = (17, 17, 17)
RED = (214, 40, 40)
BLUE = (29, 78, 137)
TINT = (233, 225, 207)
HAIR = (150, 142, 128)
WHITE = (255, 255, 255)

COL_X = [28, 191, 354, 517, 680, 843]  # 6 columns, width 151, gutter 12
COL_W = 151
RIGHT = 996


def font(name, size):
    """Load a bundled font, falling back to the system copy."""
    for base in (os.path.join(HERE, "fonts"), "/usr/share/fonts/truetype/noto"):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise FileNotFoundError(name)


F_DISPLAY = lambda s: font("NotoSerifDisplay-Black.ttf", s)   # masthead / headlines
F_SERIF = lambda s: font("NotoSerif-Regular.ttf", s)           # decks / body
F_SERIF_B = lambda s: font("NotoSerif-Bold.ttf", s)            # secondary headlines
F_SERIF_I = lambda s: font("NotoSerif-Italic.ttf", s)          # captions
F_COND = lambda s: font("NotoSansCondensed-Bold.ttf", s)       # banner / labels


def wrap(text, fnt, max_w):
    """Greedy word wrap to max_w pixels; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def cover(im, tw, th, focus_y=0.5):
    """Resize + centre-crop an image to exactly tw x th (focus_y: 0 top, 1 bottom)."""
    iw, ih = im.size
    scale = max(tw / iw, th / ih)
    im = im.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = round((im.height - th) * focus_y)
    return im.crop((x, y, x + tw, y + th))


def rule(draw, x0, x1, y, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- 1. top ticker strip -------------------------------------------
    ticker = ("WEDNESDAY, 25 NOVEMBER 2026    ·    WORLD EDITION    ·    "
              "EIGHT STORIES FROM SIX REGIONS")
    f_ticker = F_COND(14)
    assert f_ticker.getlength(ticker) <= W - 2 * M, "ticker too wide"
    text(d, (W // 2, 10), ticker, f_ticker, anchor="mt")
    rule(d, M, RIGHT, 36)

    # ---- 2. masthead + double rule --------------------------------------
    f_mast = F_DISPLAY(76)
    assert f_mast.getlength("THE WORLD DISPATCH") <= W - 2 * M, "masthead too wide"
    # Centre the masthead ink in the band between the ticker rule (y=36)
    # and the double rule (y=128), biased 2px up: the old y=44 put the caps'
    # baseline 1px above the rule. textbbox measures the real ink box, so
    # this stays centred even if the font changes.
    _bb = d.textbbox((0, 0), "THE WORLD DISPATCH", f_mast, anchor="la")
    _ink_h = _bb[3] - _bb[1]
    _ink_top = 36 + (128 - 36 - _ink_h) // 2 - 2
    text(d, (W // 2, _ink_top - _bb[1]), "THE WORLD DISPATCH", f_mast, anchor="ma")
    rule(d, M, RIGHT, 128, width=3)
    rule(d, M, RIGHT, 133, width=1)

    # ---- 3. red BREAKING banner ------------------------------------------
    d.rectangle([M, 142, RIGHT, 180], fill=RED)
    f_break = F_COND(23)
    text(d, (44, 161), "BREAKING", f_break, fill=WHITE, anchor="lm")
    d.line([(186, 150), (186, 172)], fill=WHITE, width=1)
    f_kick = F_COND(21)
    banner = "IRAN SAYS TWO TANKERS HIT MINES IN HORMUZ"
    assert f_kick.getlength(banner) <= RIGHT - 200, "banner too wide"
    text(d, (200, 161), banner, f_kick, fill=WHITE, anchor="lm")

    # ---- 4. hero image (cols 1-4) ----------------------------------------
    hero = Image.open(os.path.join(HERE, "assets", "hero.png")).convert("RGB")
    page.paste(cover(hero, 640, 260), (M, 190))
    d.rectangle([M, 190, M + 640, 450], outline=INK, width=1)
    f_cap = F_SERIF_I(13)
    caption = ("Iran's Guards Navy says two tankers struck mines and caught fire.")
    assert f_cap.getlength(caption) <= 640, "caption too wide"
    text(d, (M, 458), caption, f_cap)

    # ---- 5. lead kicker / headline / deck --------------------------------
    text(d, (M, 486), "IRAN SAYS  ·  STRAIT OF HORMUZ  ·  25 NOVEMBER 2026",
         F_COND(15), fill=RED)
    # Two-line lead at full spec size (44px).
    text(d, (M, 504), "TWO TANKERS HIT", F_DISPLAY(44))
    text(d, (M, 552), "MINES IN HORMUZ", F_DISPLAY(44))
    deck_lines = wrap(
        "Tehran says the tankers took an unauthorised route; the U.S. tells "
        "citizens to leave Iran.",
        F_SERIF(17), 640)
    assert len(deck_lines) <= 2, f"lead deck wraps to {len(deck_lines)} lines"
    y = 606
    for line in deck_lines:
        text(d, (M, y), line, F_SERIF(17))
        y += 22
    assert y <= 664, "lead deck collides with lower band"

    # ---- 6. sidebar "AROUND THE WORLD" (cols 5-6) -----------------------
    sx0, sx1 = 680, RIGHT
    d.rectangle([sx0, 190, sx1, 640], fill=TINT, outline=INK, width=1)
    text(d, (696, 202), "AROUND THE WORLD", F_COND(18))
    rule(d, 696, 980, 228, width=2, fill=RED)
    briefs = [
        ("01", "UNITED STATES",
         "U.S. tells citizens to leave Iran",
         "Virtual Embassy warns hostilities could escalate rapidly."),
        ("02", "EUROPE",
         "Leak puts Russian war dead past 490,000",
         "BBC analysis of leaked Rosstat records; the toll may near 700,000."),
        ("03", "SOUTH ASIA",
         "Bangladesh raises garment wage 36%",
         "Board sets 17,000 taka after weeks of protests shut factories."),
        ("04", "PACIFIC",
         "Solomons reject foreign bases",
         "Canberra treaty makes Australia the primary security partner."),
    ]
    # Measure every brief, then spread the spare space evenly so the tinted
    # box is filled instead of ending in a dead band.
    measured = []
    for num, tag, head, deck in briefs:
        hl = wrap(head, F_SERIF_B(18), 284)
        assert len(hl) <= 2, f"sidebar headline wraps to {len(hl)}: {head!r}"
        dl = wrap(deck, F_SERIF(13), 284)
        assert len(dl) <= 2, f"sidebar deck wraps to {len(dl)}: {deck!r}"
        measured.append((num, tag, hl, dl))
    content_h = [21 + len(hl) * 22 + 2 + len(dl) * 15
                 for _, _, hl, dl in measured]
    gap = max(8, (632 - 242 - sum(content_h)) // 3)
    by = 242
    for i, ((num, tag, hl, dl), ch) in enumerate(zip(measured, content_h)):
        text(d, (696, by), num, F_COND(15), fill=RED)
        text(d, (724, by), tag, F_COND(13))
        hy = by + 21
        for line in hl:
            text(d, (696, hy), line, F_SERIF_B(18))
            hy += 22
        dy = hy + 2
        for line in dl:
            text(d, (696, dy), line, F_SERIF(13))
            dy += 15
        by = by + ch + gap
        if i < 3:
            rule(d, 696, 980, by - gap + 8, width=1, fill=HAIR)
    assert by - gap <= 640, f"sidebar overflows its box (ends {by - gap})"

    # ---- 7. lower band: three story modules ------------------------------
    text(d, (M, 664), "MORE FROM WEDNESDAY", F_COND(14))
    rule(d, M, RIGHT, 686, width=1)
    modules = [
        ("rescue.png", "AMERICAS", "All hostages freed in Cartagena raid",
         "Forces storm the Éxito supermarket after a day-long siege; one "
         "captor killed."),
        ("mine.png", "ASIA", "Flooded Bogor gold mine traps miners",
         "Rescuers race to reach dozens trapped 100 metres underground."),
        ("space.png", "SPACE", "Pakistan's first astronaut reaches orbit",
         "Shenzhou-24 docks with Tiangong; Zeeshan Ali is the first foreigner "
         "aboard."),
    ]
    for i, (fname, kicker, head, deck) in enumerate(modules):
        mx = COL_X[i * 2]
        im = Image.open(os.path.join(HERE, "assets", fname)).convert("RGB")
        page.paste(cover(im, 314, 140), (mx, 698))
        d.rectangle([mx, 698, mx + 314, 838], outline=INK, width=1)
        text(d, (mx, 850), kicker, F_COND(12), fill=RED)
        hl = wrap(head, F_SERIF_B(21), 314)
        assert len(hl) <= 2, f"module headline wraps to {len(hl)}: {head!r}"
        hy = 868
        for line in hl:
            text(d, (mx, hy), line, F_SERIF_B(21))
            hy += 25
        dl = wrap(deck, F_SERIF(14), 314)
        assert len(dl) <= 2, f"module deck wraps to {len(dl)}: {deck!r}"
        dy = hy + 2
        for line in dl:
            text(d, (mx, dy), line, F_SERIF(14))
            dy += 18
        assert dy <= 972, f"module {i} overflows into footer (ends {dy})"

    # ---- 8. footer markets ticker ----------------------------------------
    # NOTE: Noto Sans Condensed has no U+2212 minus sign — use ASCII hyphen.
    rule(d, M, RIGHT, 974, width=1)
    footer = ("MARKETS  ·  WEDNESDAY  ·  KOSPI -6.16%  ·  NIKKEI -2.78%  ·  "
              "BRENT $90.97 -0.5%")
    assert F_COND(13).getlength(footer) <= W - 2 * M, "footer too wide"
    text(d, (W // 2, 986), footer, F_COND(13), anchor="mt")

    out = os.path.join(HERE, "image.png")
    page.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
