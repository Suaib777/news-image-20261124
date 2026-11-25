#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: one 1024x1024 front-page summary of
Tuesday 24 November 2026, drawn from the day's verified headlines.

Stories (all reported on 24 Nov 2026, verified against live news sources):
 1. Houthis hit Riyadh's tallest tower, 11 wounded (2nd strike in a week)
 2. Israeli strikes kill at least six in Gaza, incl. Hamas security chief
 3. NATO vows space defence after reports of a Russian nuclear satellite
 4. Russian warplanes enter Korea's air defence zone; Ulleung alert
 5. WHO staff evacuated from Akwe as fighting hits DRC Ebola response
 6. Nvidia gives back $240B after Monday's record 31% surge
 7. US-Qatar talks continue as Iran talks stay stalled

Everything is drawn with PIL primitives (no photos, no stock, no network).
Run: python3 gen_image.py  -> writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
NAVY = (14, 42, 71)
NAVY_LT = (27, 68, 106)
GOLD = (217, 164, 65)
RED = (178, 44, 36)
TEAL = (31, 122, 109)
SKY = (127, 179, 213)
SKY_LT = (214, 233, 244)
CARD = (255, 255, 255)
GREY = (110, 110, 105)
LINE = (200, 192, 175)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def kicker(draw, x, y, label, color):
    f = font(SANS_B, 21)
    tw = draw.textlength(label, font=f) + 18
    draw.rounded_rectangle([x, y, x + tw, y + 30], radius=4, fill=color)
    draw.text((x + 9, y + 4), label, font=f, fill=(255, 255, 255))


def icon_disc(draw, cx, cy, r, bg):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg)


def icon_tower(d, cx, cy, r):
    """Tall skyscraper with a strike burst at its crown."""
    icon_disc(d, cx, cy, r, SKY_LT)
    # tower body
    d.polygon([(cx - r * 0.30, cy + r * 0.62), (cx - r * 0.30, cy - r * 0.55),
               (cx + r * 0.30, cy - r * 0.55), (cx + r * 0.30, cy + r * 0.62)],
              fill=NAVY)
    # crown step
    d.rectangle([cx - r * 0.38, cy - r * 0.55, cx + r * 0.38, cy - r * 0.42], fill=NAVY)
    # windows
    for j in range(5):
        yy = cy - r * 0.30 + j * r * 0.20
        for i in (-1, 1):
            xx = cx + i * r * 0.14 - r * 0.05
            d.rectangle([xx, yy, xx + r * 0.10, yy + r * 0.09], fill=GOLD)
    # burst at the crown
    bx, by = cx + r * 0.42, cy - r * 0.62
    d.polygon([(bx, by - r * 0.30), (bx + r * 0.10, by - r * 0.08),
               (bx + r * 0.30, by - r * 0.10), (bx + r * 0.14, by + r * 0.08),
               (bx + r * 0.26, by + r * 0.28), (bx, by + r * 0.14),
               (bx - r * 0.26, by + r * 0.28), (bx - r * 0.14, by + r * 0.08),
               (bx - r * 0.30, by - r * 0.10), (bx - r * 0.10, by - r * 0.08)],
              fill=(230, 120, 30))
    d.rectangle([cx - r * 0.62, cy + r * 0.62, cx + r * 0.62, cy + r * 0.72], fill=NAVY_LT)


def icon_blast(d, cx, cy, r):
    """Explosion burst on a dark disc."""
    icon_disc(d, cx, cy, r, (60, 60, 60))
    d.polygon([(cx, cy - r * 0.72), (cx + r * 0.18, cy - r * 0.22),
               (cx + r * 0.70, cy - r * 0.42), (cx + r * 0.38, cy - r * 0.02),
               (cx + r * 0.72, cy + r * 0.30), (cx + r * 0.24, cy + r * 0.28),
               (cx + r * 0.34, cy + r * 0.70), (cx, cy + r * 0.38),
               (cx - r * 0.34, cy + r * 0.70), (cx - r * 0.24, cy + r * 0.28),
               (cx - r * 0.72, cy + r * 0.30), (cx - r * 0.38, cy - r * 0.02),
               (cx - r * 0.70, cy - r * 0.42), (cx - r * 0.18, cy - r * 0.22)],
              fill=(240, 160, 40))
    d.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22],
              fill=(255, 230, 150))


def icon_satellite(d, cx, cy, r):
    """Satellite with solar panels and an orbit ring."""
    icon_disc(d, cx, cy, r, SKY_LT)
    d.arc([cx - r * 0.92, cy - r * 0.92, cx + r * 0.92, cy + r * 0.92],
          200, 340, fill=NAVY_LT, width=5)
    # panels
    d.rectangle([cx - r * 0.78, cy - r * 0.16, cx - r * 0.22, cy + r * 0.16],
                fill=NAVY)
    d.rectangle([cx + r * 0.22, cy - r * 0.16, cx + r * 0.78, cy + r * 0.16],
                fill=NAVY)
    # body
    d.rounded_rectangle([cx - r * 0.24, cy - r * 0.30, cx + r * 0.24, cy + r * 0.30],
                        radius=int(r * 0.08), fill=RED)
    d.rectangle([cx - r * 0.24, cy - r * 0.30, cx - r * 0.06, cy + r * 0.30],
                fill=(120, 20, 15))
    # dish
    d.polygon([(cx + r * 0.10, cy - r * 0.30), (cx + r * 0.34, cy - r * 0.52),
               (cx + r * 0.30, cy - r * 0.22)], fill=GOLD)


def icon_jet(d, cx, cy, r):
    """Fighter jet, top view, on a sky disc."""
    icon_disc(d, cx, cy, r, SKY_LT)
    # fuselage
    d.polygon([(cx, cy - r * 0.78), (cx + r * 0.14, cy - r * 0.30),
               (cx + r * 0.12, cy + r * 0.55), (cx, cy + r * 0.72),
               (cx - r * 0.12, cy + r * 0.55), (cx - r * 0.14, cy - r * 0.30)],
              fill=NAVY)
    # delta wings
    d.polygon([(cx - r * 0.10, cy - r * 0.05), (cx - r * 0.85, cy + r * 0.42),
               (cx - r * 0.85, cy + r * 0.58), (cx - r * 0.08, cy + r * 0.30)],
              fill=NAVY_LT)
    d.polygon([(cx + r * 0.10, cy - r * 0.05), (cx + r * 0.85, cy + r * 0.42),
               (cx + r * 0.85, cy + r * 0.58), (cx + r * 0.08, cy + r * 0.30)],
              fill=NAVY_LT)
    # tail fins
    d.polygon([(cx - r * 0.10, cy + r * 0.42), (cx - r * 0.34, cy + r * 0.68),
               (cx - r * 0.16, cy + r * 0.68)], fill=NAVY)
    d.polygon([(cx + r * 0.10, cy + r * 0.42), (cx + r * 0.34, cy + r * 0.68),
               (cx + r * 0.16, cy + r * 0.68)], fill=NAVY)
    # cockpit
    d.ellipse([cx - r * 0.06, cy - r * 0.52, cx + r * 0.06, cy - r * 0.28],
              fill=(255, 255, 255))


def icon_medical(d, cx, cy, r):
    """Red cross on a white disc."""
    icon_disc(d, cx, cy, r, (255, 255, 255))
    d.rectangle([cx - r * 0.20, cy - r * 0.62, cx + r * 0.20, cy + r * 0.62],
                fill=RED)
    d.rectangle([cx - r * 0.62, cy - r * 0.20, cx + r * 0.62, cy + r * 0.20],
                fill=RED)


def icon_chart(d, cx, cy, r):
    icon_disc(d, cx, cy, r, (252, 228, 228))
    vals = [0.78, 0.60, 0.66, 0.42, 0.48, 0.22]
    bw = r * 1.5 / len(vals)
    for i, v in enumerate(vals):
        x0 = cx - r * 0.75 + i * bw + 2
        d.rectangle([x0, cy + r * 0.55 - v * r * 1.0, x0 + bw - 5, cy + r * 0.55], fill=RED)
    d.line([cx - r * 0.7, cy - r * 0.55, cx + r * 0.7, cy - r * 0.05], fill=NAVY, width=6)
    d.polygon([(cx + r * 0.7, cy - r * 0.05), (cx + r * 0.38, cy - r * 0.10),
               (cx + r * 0.62, cy + r * 0.22)], fill=NAVY)


def icon_chat(d, cx, cy, r):
    """Two overlapping speech bubbles (talks)."""
    icon_disc(d, cx, cy, r, SKY_LT)
    # back bubble
    d.rounded_rectangle([cx + r * 0.02, cy - r * 0.52, cx + r * 0.72, cy + r * 0.10],
                        radius=int(r * 0.14), fill=NAVY_LT)
    d.polygon([(cx + r * 0.16, cy + r * 0.08), (cx + r * 0.30, cy + r * 0.30),
               (cx + r * 0.36, cy + r * 0.08)], fill=NAVY_LT)
    # front bubble
    d.rounded_rectangle([cx - r * 0.72, cy - r * 0.12, cx - r * 0.02, cy + r * 0.52],
                        radius=int(r * 0.14), fill=NAVY)
    d.polygon([(cx - r * 0.36, cy + r * 0.50), (cx - r * 0.22, cy + r * 0.72),
               (cx - r * 0.16, cy + r * 0.50)], fill=NAVY)
    # dots
    for i in range(3):
        xx = cx - r * 0.56 + i * r * 0.20
        d.ellipse([xx, cy + r * 0.12, xx + r * 0.09, cy + r * 0.21], fill=(255, 255, 255))


def story_card(d, x, y, w, h, kicker_label, kicker_color, headline, caption, icon_fn,
               headline_size=28, icon_r=32, caption_size=20):
    """Card with kicker + small icon on the top row, headline and caption
    spanning the full card width below (no text/icon overlap)."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=LINE, width=2)
    pad = 22
    icon_fn(d, x + w - 52, y + 34, icon_r)
    kicker(d, x + pad, y + 16, kicker_label, kicker_color)
    tx = x + pad
    tw = w - 2 * pad
    hf = font(SANS_B, headline_size)
    lines = wrap(d, headline, hf, tw)
    ly = y + 58
    for ln in lines[:2]:
        d.text((tx, ly), ln, font=hf, fill=INK)
        ly += headline_size + 5
    cf = font(SANS, caption_size)
    for ln in wrap(d, caption, cf, tw)[:2]:
        d.text((tx, ly + 4), ln, font=cf, fill=GREY)
        ly += caption_size + 6


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 160], fill=NAVY)
    d.rectangle([0, 160, W, 166], fill=GOLD)
    draw_center(d, W // 2, 18, "THE WORLD IN ONE DAY", font(SERIF_B, 58), (255, 255, 255))
    draw_center(d, W // 2, 96, "T U E S D A Y   2 4   N O V E M B E R   2 0 2 6",
                font(SANS_B, 28), GOLD)

    # ---- lead story ----
    lx, ly, lw, lh = 28, 182, W - 56, 246
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=CARD, outline=LINE, width=2)
    d.rectangle([lx, ly + 10, lx + 10, ly + lh - 10], fill=RED)
    kicker(d, lx + 30, ly + 16, "MIDDLE EAST", RED)
    icon_tower(d, lx + lw - 108, ly + 122, 80)
    hf = font(SANS_B, 42)
    lines = wrap(d, "HOUTHIS HIT RIYADH'S TALLEST TOWER", hf, lw - 280)
    y = ly + 54
    for ln in lines:
        d.text((lx + 30, y), ln, font=hf, fill=INK)
        y += 50
    cf = font(SANS, 24)
    for ln in wrap(d, "Drone strike wounds 11 in the financial district — the second hit in a week.",
                   cf, lw - 280):
        d.text((lx + 30, y + 4), ln, font=cf, fill=GREY)
        y += 30

    # ---- grid rows ----
    gw = (W - 56 - 20) // 2  # 474
    story_card(d, 28, 444, gw, 192, "WAR", NAVY,
               "GAZA STRIKES KILL AT LEAST SIX",
               "Hamas security chief among the dead as the ceasefire frays.", icon_blast)
    story_card(d, 28 + gw + 20, 444, gw, 192, "SECURITY", NAVY_LT,
               "NATO VOWS SPACE DEFENCE",
               "Rutte answers reports of a Russian nuclear satellite, 'Sputnik-S'.", icon_satellite)
    story_card(d, 28, 652, gw, 192, "MARKETS", RED,
               "NVIDIA GIVES BACK $240 BILLION",
               "Shares fall 5.9% a day after a record 31% surge.", icon_chart)
    story_card(d, 28 + gw + 20, 652, gw, 192, "HEALTH", TEAL,
               "EBOLA: WHO STAFF EVACUATED",
               "Fighting in Ituri forces medics out of Akwe hospital.", icon_medical)

    # ---- bottom row (slim cards, one-line headlines) ----
    story_card(d, 28, 860, gw, 136, "ASIA", (150, 90, 20),
               "RUSSIAN JETS NEAR KOREA",
               "Ulleung Island alert lifted in minutes.", icon_jet,
               headline_size=27, icon_r=30)
    story_card(d, 28 + gw + 20, 860, gw, 136, "DIPLOMACY", (90, 130, 40),
               "US-QATAR TALKS CONTINUE",
               "US-Qatar dialogue as Iran talks stall.", icon_chat,
               headline_size=27, icon_r=30)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
