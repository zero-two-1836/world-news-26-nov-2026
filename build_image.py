#!/usr/bin/env python3
"""Draw the World Today front page for Thursday, 26 November 2026.

Fresh artwork for the make.fun news-image-20261126 entry. All ten
stories were cross-checked against at least two independent sources
(see README.md). Everything is drawn with Pillow primitives only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

NAVY = (13, 27, 62)
NAVY2 = (24, 48, 96)
GOLD = (212, 160, 32)
CREAM = (250, 246, 236)
INK = (18, 22, 30)
GREY = (92, 98, 110)
RED = (178, 34, 34)
TEAL = (14, 122, 110)
ORANGE = (214, 92, 24)
SKY = (168, 205, 226)
SMOKE = (120, 122, 128)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANS_OB = lambda s: font("DejaVuSerif.ttf", s)  # no Sans oblique on system


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def draw_refinery(d, x0, y0, x1, y1):
    """Simple stylised refinery at dusk: sky, towers, flame, smoke."""
    d.rectangle([x0, y0, x1, y1], fill=(38, 58, 86))
    # sun glow, top-left corner
    d.ellipse([x0 + 16, y0 + 14, x0 + 76, y0 + 74], fill=(232, 164, 60))
    # ground
    d.rectangle([x0, y1 - 42, x1, y1], fill=(20, 30, 48))
    # storage tanks
    for tx in (x0 + 18, x0 + 96):
        d.rectangle([tx, y1 - 118, tx + 64, y1 - 42], fill=(210, 214, 220))
        d.ellipse([tx, y1 - 132, tx + 64, y1 - 104], fill=(232, 236, 240))
    # distillation tower
    d.polygon([(x0 + 200, y1 - 42), (x0 + 212, y1 - 168),
               (x0 + 232, y1 - 168), (x0 + 244, y1 - 42)], fill=(150, 158, 168))
    d.rectangle([x0 + 206, y1 - 150, x0 + 238, y1 - 142], fill=(120, 126, 134))
    d.rectangle([x0 + 206, y1 - 116, x0 + 238, y1 - 108], fill=(120, 126, 134))
    # flare stack with flame
    d.rectangle([x0 + 268, y1 - 190, x0 + 278, y1 - 42], fill=(96, 102, 112))
    d.polygon([(x0 + 262, y1 - 190), (x0 + 273, y1 - 236),
               (x0 + 284, y1 - 190)], fill=(240, 120, 30))
    d.polygon([(x0 + 267, y1 - 192), (x0 + 273, y1 - 214),
               (x0 + 279, y1 - 192)], fill=(250, 200, 60))
    # smoke plume, kept fully inside the panel
    cx = x0 + 150
    for i, r in enumerate((26, 32, 36, 38)):
        cy = y0 + 46 + i * 30
        d.ellipse([cx - r + i * 8, cy - r, cx + r + i * 8, cy + r],
                  fill=SMOKE)
    d.ellipse([cx - 16, y0 + 128, cx + 40, y0 + 168], fill=(96, 98, 104))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 124], fill=GOLD)
    d.text((28, 14), "THE WORLD TODAY", font=F_SERIF_B(54), fill=(255, 255, 255))
    d.text((28, 78), "Thursday, 26 November 2026", font=F_SANS_B(24),
           fill=(232, 196, 90))
    d.text((W - 28, 82), "10 STORIES  •  ONE DAY", font=F_SANS_B(17),
           fill=(190, 200, 220), anchor="ra")

    # ---- Hero -----------------------------------------------------
    hx, hy, hw = 28, 140, 600
    d.text((hx, hy), "TOP STORY  —  MIDDLE EAST", font=F_SANS_B(19), fill=RED)
    y = hy + 32
    y = para(d, hx, y, "Houthis claim strike on Saudi Arabia's largest oil refinery",
             F_SERIF_B(40), INK, hw, 48)
    y += 6
    y = para(d, hx, y,
             "Satellite images show a huge smoke plume over Ras Tanura. "
             "Riyadh says four drones were shot down; Brent crude jumps "
             "past $93 a barrel.",
             F_SANS(20), (52, 58, 70), hw, 27)
    # hero art panel
    draw_refinery(d, 656, 140, 996, 400)
    d.rectangle([656, 140, 996, 400], outline=NAVY, width=3)
    d.text((656, 406), "Ras Tanura — smoke seen from space",
           font=F_SANS_OB(15), fill=GREY)

    # ---- Divider --------------------------------------------------
    d.line([(28, 436), (996, 436)], fill=GOLD, width=3)

    # ---- Story grid: 3 x 3 ---------------------------------------
    stories = [
        ("CAIRO", RED, "Fuel tanker fire kills at least 30",
         "Blaze engulfs cars on the Cairo ring road; the toll may still rise."),
        ("SPACE", TEAL, "First Pakistani in orbit reaches Tiangong",
         "Shenzhou-24 docks; Zeeshan Ali is the first foreign visitor to China's station."),
        ("BANGLADESH", ORANGE, "Garment wages up 36% after protests",
         "Minimum pay rises to 17,000 taka a month; workers say it is still too little."),
        ("KOREA", NAVY2, "Pyongyang expels Swiss envoy",
         "North Korea shuts the Swiss office opened a month ago, over camp sanctions."),
        ("GAZA", RED, "Israeli strike kills Hamas security chief",
         "Abuelouf, his wife and two daughters die; a second senior official killed in a day."),
        ("THE GULF", NAVY2, "Two tankers hit mines in Hormuz",
         "Iran says the ships struck mines on an unauthorised route; the claims are unverified."),
        ("USA", TEAL, "Six die in plane crash off Mississippi",
         "Cessna 210 plunges into the Gulf of Mexico; two boys among the dead."),
        ("CHESS", ORANGE, "Gukesh–Sindarov: 20-move draw",
         "World title match level at 1–1 after one of the shortest games in years."),
        ("CRICKET", TEAL, "15-year-old smashes 204 off 53 balls",
         "Sooryavanshi sets List A records for the fastest century and double century."),
    ]
    gx, gy = 28, 452
    cw, ch, gap = 312, 158, 16
    for i, (tag, color, head, summ) in enumerate(stories):
        col, row = i % 3, i // 3
        x = gx + col * (cw + gap)
        yy = gy + row * (ch + gap)
        d.rectangle([x, yy, x + cw, yy + ch], fill=(255, 255, 255),
                    outline=(205, 210, 218), width=2)
        d.rectangle([x, yy, x + cw, yy + 6], fill=color)
        d.text((x + 14, yy + 16), tag, font=F_SANS_B(15), fill=color)
        ty = para(d, x + 14, yy + 40, head, F_SANS_B(21), INK, cw - 28, 25)
        para(d, x + 14, ty + 4, summ, F_SANS(15), GREY, cw - 28, 19)

    # ---- Footer ---------------------------------------------------
    fy = 968
    d.line([(28, fy), (996, fy)], fill=(205, 210, 218), width=2)
    d.text((28, fy + 12),
           "Sources: Reuters, AP, Xinhua, Yonhap, ChessBase, ESPNcricinfo — every story",
           font=F_SANS(15), fill=GREY)
    d.text((28, fy + 32),
           "cross-checked against at least two independent sources.  •  theworldtoday • 26 Nov 2026",
           font=F_SANS(15), fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
