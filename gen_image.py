#!/usr/bin/env python3
"""news-image-20261124: one 1024x1024 front page summing up Tuesday
24 November 2026.

Seven stories, each verified against live news sources on 24 Nov 2026:
 1. Houthis hit Riyadh's tallest tower, 11 wounded
 2. Israeli strikes kill at least six in Gaza
 3. NATO vows space defence after Russian nuclear-satellite reports
 4. Russian warplanes enter Korea's air defence zone
 5. WHO staff evacuated as fighting hits the DRC Ebola response
 6. Nvidia gives back $240B after Monday's record surge
 7. US-Qatar talks continue as Iran talks stall

Drawn with PIL primitives only (no photos, no network).
Run: python3 gen_image.py  -> writes entry.png beside this file.

Sources checked 24 Nov 2026: Reuters (Riyadh, Nvidia), AFP (Gaza toll),
AP / dpa (Rutte space defence, Berlin), Yonhap (KADIZ, Ulleung), WHO /
MSF bulletins (DRC Ebola, Akwe), US State Department (US-Qatar dialogue).
Layout: masthead 160px, lead card 246px, 2x2 grid of 192px cards, two
136px slim cards at the bottom; headline and caption wrap to two lines max.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

PALETTE = {
    "paper": (248, 244, 233),
    "ink": (20, 20, 20),
    "navy": (14, 42, 71),
    "navy_lt": (27, 68, 106),
    "gold": (217, 164, 65),
    "red": (178, 44, 36),
    "teal": (31, 122, 109),
    "sky_lt": (214, 233, 244),
    "card": (255, 255, 255),
    "grey": (110, 110, 105),
    "line": (200, 192, 175),
    "flame": (230, 120, 30),
    "copper": (184, 115, 51),
    "brown": (150, 90, 20),
    "green": (90, 130, 40),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
FONTS = {
    "serif_b": FONT_DIR + "DejaVuSerif-Bold.ttf",
    "sans_b": FONT_DIR + "DejaVuSans-Bold.ttf",
    "sans": FONT_DIR + "DejaVuSans.ttf",
}


def load(kind, size):
    return ImageFont.truetype(FONTS[kind], size)


def fit(d, text, fnt, width):
    """Greedy word wrap: lines that fit inside width."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if not cur or d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def centred(d, cx, y, text, kind, size, colour):
    fnt = load(kind, size)
    half = d.textlength(text, font=fnt) / 2
    d.text((cx - half, y), text, font=fnt, fill=colour)


def tag(d, x, y, label, colour):
    fnt = load("sans_b", 21)
    box_w = d.textlength(label, font=fnt) + 18
    d.rounded_rectangle((x, y, x + box_w, y + 30), radius=4, fill=colour)
    d.text((x + 9, y + 4), label, font=fnt, fill=(255, 255, 255))


def disc(d, cx, cy, r, colour):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=colour)


def glyph_tower(d, cx, cy, r):
    """Tall skyscraper with a strike burst at its crown."""
    P = PALETTE
    disc(d, cx, cy, r, P["sky_lt"])
    x0, x1 = cx - r * 0.30, cx + r * 0.30
    top, bot = cy - r * 0.55, cy + r * 0.62
    d.polygon([(x0, bot), (x0, top), (x1, top), (x1, bot)], fill=P["navy"])
    d.rectangle((cx - r * 0.38, top, cx + r * 0.38, top + r * 0.13), fill=P["navy"])
    for j in range(5):
        yy = cy - r * 0.30 + j * r * 0.20
        for s in (-1, 1):
            xx = cx + s * r * 0.14 - r * 0.05
            d.rectangle((xx, yy, xx + r * 0.10, yy + r * 0.09), fill=P["gold"])
    bx, by = cx + r * 0.42, cy - r * 0.62
    pts = [(0, -0.30), (0.10, -0.08), (0.30, -0.10), (0.14, 0.08),
           (0.26, 0.28), (0, 0.14), (-0.26, 0.28), (-0.14, 0.08),
           (-0.30, -0.10), (-0.10, -0.08)]
    d.polygon([(bx + a * r, by + b * r) for a, b in pts], fill=P["flame"])
    d.rectangle((cx - r * 0.62, bot, cx + r * 0.62, bot + r * 0.10),
                fill=P["navy_lt"])


def glyph_blast(d, cx, cy, r):
    """Explosion burst on a dark disc."""
    disc(d, cx, cy, r, (60, 60, 60))
    spikes = [(0, -0.72), (0.18, -0.22), (0.70, -0.42), (0.38, -0.02),
              (0.72, 0.30), (0.24, 0.28), (0.34, 0.70), (0, 0.38),
              (-0.34, 0.70), (-0.24, 0.28), (-0.72, 0.30), (-0.38, -0.02),
              (-0.70, -0.42), (-0.18, -0.22)]
    d.polygon([(cx + a * r, cy + b * r) for a, b in spikes], fill=(240, 160, 40))
    disc(d, cx, cy, r * 0.22, (255, 230, 150))


def glyph_satellite(d, cx, cy, r):
    """Satellite with solar panels and an orbit ring."""
    P = PALETTE
    disc(d, cx, cy, r, P["sky_lt"])
    d.arc((cx - r * 0.92, cy - r * 0.92, cx + r * 0.92, cy + r * 0.92),
          200, 340, fill=P["navy_lt"], width=5)
    d.rectangle((cx - r * 0.78, cy - r * 0.16, cx - r * 0.22, cy + r * 0.16),
                fill=P["navy"])
    d.rectangle((cx + r * 0.22, cy - r * 0.16, cx + r * 0.78, cy + r * 0.16),
                fill=P["navy"])
    d.rounded_rectangle((cx - r * 0.24, cy - r * 0.30, cx + r * 0.24, cy + r * 0.30),
                        radius=int(r * 0.08), fill=P["red"])
    d.rectangle((cx - r * 0.24, cy - r * 0.30, cx - r * 0.06, cy + r * 0.30),
                fill=(120, 20, 15))
    d.polygon([(cx + r * 0.10, cy - r * 0.30), (cx + r * 0.34, cy - r * 0.52),
               (cx + r * 0.30, cy - r * 0.22)], fill=P["gold"])


def glyph_jet(d, cx, cy, r):
    """Fighter jet, top view, on a sky disc."""
    P = PALETTE
    disc(d, cx, cy, r, P["sky_lt"])
    body = [(0, -0.78), (0.14, -0.30), (0.12, 0.55), (0, 0.72),
            (-0.12, 0.55), (-0.14, -0.30)]
    d.polygon([(cx + a * r, cy + b * r) for a, b in body], fill=P["navy"])
    left_wing = [(-0.10, -0.05), (-0.85, 0.42), (-0.85, 0.58), (-0.08, 0.30)]
    right_wing = [(0.10, -0.05), (0.85, 0.42), (0.85, 0.58), (0.08, 0.30)]
    for wing in (left_wing, right_wing):
        d.polygon([(cx + a * r, cy + b * r) for a, b in wing], fill=P["navy_lt"])
    for s in (-1, 1):
        fin = [(s * 0.10, 0.42), (s * 0.34, 0.68), (s * 0.16, 0.68)]
        d.polygon([(cx + a * r, cy + b * r) for a, b in fin], fill=P["navy"])
    d.ellipse((cx - r * 0.06, cy - r * 0.52, cx + r * 0.06, cy - r * 0.28),
              fill=(255, 255, 255))


def glyph_medical(d, cx, cy, r):
    """Red cross on a white disc."""
    disc(d, cx, cy, r, (255, 255, 255))
    red = PALETTE["red"]
    d.rectangle((cx - r * 0.20, cy - r * 0.62, cx + r * 0.20, cy + r * 0.62),
                fill=red)
    d.rectangle((cx - r * 0.62, cy - r * 0.20, cx + r * 0.62, cy + r * 0.20),
                fill=red)


def glyph_chart(d, cx, cy, r):
    """Falling bars with a down-trend arrow."""
    P = PALETTE
    disc(d, cx, cy, r, (252, 228, 228))
    vals = [0.78, 0.60, 0.66, 0.42, 0.48, 0.22]
    bw = r * 1.5 / len(vals)
    for i, v in enumerate(vals):
        x0 = cx - r * 0.75 + i * bw + 2
        d.rectangle((x0, cy + r * 0.55 - v * r, x0 + bw - 5, cy + r * 0.55),
                    fill=P["red"])
    d.line((cx - r * 0.7, cy - r * 0.55, cx + r * 0.7, cy - r * 0.05),
           fill=P["navy"], width=6)
    d.polygon([(cx + r * 0.7, cy - r * 0.05), (cx + r * 0.38, cy - r * 0.10),
               (cx + r * 0.62, cy + r * 0.22)], fill=P["navy"])


def glyph_chat(d, cx, cy, r):
    """Two overlapping speech bubbles (talks)."""
    P = PALETTE
    disc(d, cx, cy, r, P["sky_lt"])
    d.rounded_rectangle((cx + r * 0.02, cy - r * 0.52, cx + r * 0.72, cy + r * 0.10),
                        radius=int(r * 0.14), fill=P["navy_lt"])
    d.polygon([(cx + r * 0.16, cy + r * 0.08), (cx + r * 0.30, cy + r * 0.30),
               (cx + r * 0.36, cy + r * 0.08)], fill=P["navy_lt"])
    d.rounded_rectangle((cx - r * 0.72, cy - r * 0.12, cx - r * 0.02, cy + r * 0.52),
                        radius=int(r * 0.14), fill=P["navy"])
    d.polygon([(cx - r * 0.36, cy + r * 0.50), (cx - r * 0.22, cy + r * 0.72),
               (cx - r * 0.16, cy + r * 0.50)], fill=P["navy"])
    for i in range(3):
        xx = cx - r * 0.56 + i * r * 0.20
        d.ellipse((xx, cy + r * 0.12, xx + r * 0.09, cy + r * 0.21),
                  fill=(255, 255, 255))


LEAD = {
    "kicker": "MIDDLE EAST",
    "colour": "red",
    "head": "HOUTHIS HIT RIYADH'S TALLEST TOWER",
    "cap": "Drone strike wounds 11 in the financial district — the second hit in a week.",
    "glyph": glyph_tower,
}

GRID = [
    {"kicker": "WAR", "colour": "navy",
     "head": "GAZA STRIKES KILL AT LEAST SIX",
     "cap": "Hamas security chief among the dead as the ceasefire frays.",
     "glyph": glyph_blast},
    {"kicker": "SECURITY", "colour": "navy_lt",
     "head": "NATO VOWS SPACE DEFENCE",
     "cap": "Rutte answers reports of a Russian nuclear satellite, 'Sputnik-S'.",
     "glyph": glyph_satellite},
    {"kicker": "MARKETS", "colour": "red",
     "head": "NVIDIA GIVES BACK $240 BILLION",
     "cap": "Shares fall 5.9% a day after a record 31% surge.",
     "glyph": glyph_chart},
    {"kicker": "HEALTH", "colour": "teal",
     "head": "EBOLA: WHO STAFF EVACUATED",
     "cap": "Fighting in Ituri forces medics out of Akwe hospital.",
     "glyph": glyph_medical},
]

BOTTOM = [
    {"kicker": "ASIA", "colour": "brown",
     "head": "RUSSIAN JETS NEAR KOREA",
     "cap": "Ulleung Island alert lifted in minutes.",
     "glyph": glyph_jet},
    {"kicker": "DIPLOMACY", "colour": "green",
     "head": "US-QATAR TALKS CONTINUE",
     "cap": "US-Qatar dialogue as Iran talks stall.",
     "glyph": glyph_chat},
]


def card(d, x, y, w, h, story, head_size=28, icon_r=32, cap_size=20):
    """Kicker + icon on the top row, headline and caption spanning the
    full card width below (no text/icon overlap)."""
    P = PALETTE
    pad = 22
    d.rounded_rectangle((x, y, x + w, y + h), radius=10, fill=P["card"],
                        outline=P["line"], width=2)
    story["glyph"](d, x + w - 52, y + 34, icon_r)
    tag(d, x + pad, y + 16, story["kicker"], P[story["colour"]])
    tx, tw = x + pad, w - 2 * pad
    hf = load("sans_b", head_size)
    ly = y + 58
    for ln in fit(d, story["head"], hf, tw)[:2]:
        d.text((tx, ly), ln, font=hf, fill=P["ink"])
        ly += head_size + 5
    cf = load("sans", cap_size)
    for ln in fit(d, story["cap"], cf, tw)[:2]:
        d.text((tx, ly + 4), ln, font=cf, fill=P["grey"])
        ly += cap_size + 6


def render():
    P = PALETTE
    img = Image.new("RGB", (W, H), P["paper"])
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle((0, 0, W, 160), fill=P["navy"])
    d.rectangle((0, 160, W, 166), fill=P["gold"])
    centred(d, W // 2, 18, "THE WORLD IN ONE DAY", "serif_b", 58, (255, 255, 255))
    centred(d, W // 2, 96, "T U E S D A Y   2 4   N O V E M B E R   2 0 2 6",
            "sans_b", 28, P["gold"])

    # ---- lead story ----
    lx, ly, lw, lh = 28, 182, W - 56, 246
    d.rounded_rectangle((lx, ly, lx + lw, ly + lh), radius=10, fill=P["card"],
                        outline=P["line"], width=2)
    d.rectangle((lx, ly + 10, lx + 10, ly + lh - 10), fill=P["red"])
    tag(d, lx + 30, ly + 16, LEAD["kicker"], P[LEAD["colour"]])
    LEAD["glyph"](d, lx + lw - 108, ly + 122, 80)
    hf = load("sans_b", 42)
    y = ly + 54
    for ln in fit(d, LEAD["head"], hf, lw - 280):
        d.text((lx + 30, y), ln, font=hf, fill=P["ink"])
        y += 50
    cf = load("sans", 24)
    for ln in fit(d, LEAD["cap"], cf, lw - 280):
        d.text((lx + 30, y + 4), ln, font=cf, fill=P["grey"])
        y += 30

    # ---- grid rows (2x2) and bottom row (slim cards) ----
    gw = (W - 56 - 20) // 2  # 474
    spots = [(28, 444), (28 + gw + 20, 444), (28, 652), (28 + gw + 20, 652)]
    for (sx, sy), story in zip(spots, GRID):
        card(d, sx, sy, gw, 192, story)
    for (sx, story) in zip((28, 28 + gw + 20), BOTTOM):
        card(d, sx, 860, gw, 136, story, head_size=27, icon_r=30)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    render()
