"""Draw the front page for 25 November 2026.

Build time only: renders entry.png (the image the entry is judged on)
from the day's headlines, written out below. No network, no input files.
Run:  python3 draw.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = 1024
MARGIN = 44
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 243, 234)      # warm newsprint
INK = (22, 22, 22)
MUTED = (90, 86, 78)
RED = (178, 34, 34)
RULE = (180, 174, 162)
BLUE = (28, 68, 120)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 52)
F_DATE = font("DejaVuSans-Bold.ttf", 18)
F_LABEL = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSerif-Bold.ttf", 33)
F_HEAD_SM = font("DejaVuSerif-Bold.ttf", 24)
F_BODY = font("DejaVuSans.ttf", 20)
F_BODY_SM = font("DejaVuSans.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 16)


def wrap(draw, text, fnt, width):
    """Wrap text into lines that fit width, word by word."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


LEAD = {
    "label": "IRAN WAR  —  LEAD",
    "headline": "Tankers burn in the Strait of Hormuz",
    "body": ("Two oil tankers strike naval mines and catch fire in the "
             "strait, Iran says. Houthi rebels claim an attack on Saudi "
             "Arabia's Ras Tanura refinery as the Gulf war widens."),
}

STORIES = [
    {
        "label": "UKRAINE",
        "color": RED,
        "headline": "Drones set two Russian refineries ablaze",
        "body": ("Ukrainian drones hit Rosneft's Syzran and Kuibyshev "
                 "refineries overnight. A Russian strike kills two in "
                 "the Odesa region and hits Kyiv."),
    },
    {
        "label": "MARKETS",
        "color": INK,
        "headline": "Asia slides; Dow tops 50,000",
        "body": ("South Korea's KOSPI plunges 6.16% and Japan's Nikkei "
                 "falls 2.78%. On Wall Street the Dow closes above "
                 "50,000 for the first time."),
    },
    {
        "label": "HUAWEI",
        "color": BLUE,
        "headline": "Huawei convicted in US fraud trial",
        "body": ("A Brooklyn jury finds the Chinese tech giant guilty "
                 "on 10 of 12 counts, including bank fraud, sanctions "
                 "violations and stealing trade secrets."),
    },
    {
        "label": "EGYPT",
        "color": RED,
        "headline": "Fuel tanker fire kills 31 near Cairo",
        "body": ("A tanker crash ignites a huge fire on a highway "
                 "outside Cairo. Egypt's Health Ministry says at "
                 "least 31 people are dead."),
    },
    {
        "label": "SUDAN",
        "color": INK,
        "headline": "RSF drone strikes kill 19 civilians",
        "body": ("Sudan's paramilitary Rapid Support Forces hit two "
                 "cities with drones, killing 19 civilians and "
                 "wounding 20, rights lawyers say."),
    },
    {
        "label": "CLIMATE",
        "color": BLUE,
        "headline": "Pope decries failure of COP31",
        "body": ("Pope Leo XIV voices concern as the UN climate talks "
                 "end with no deal. Australia and the Solomon Islands "
                 "sign a security treaty."),
    },
]

ALSO = ("Houthis claim a drone strike on a Riyadh tower injured 11; "
        "Shenzhou-24 docks with Tiangong; Colombia frees supermarket "
        "hostages; Bogor mine toll rises to six; Macy's Thanksgiving "
        "parade postponed by a storm.")


def draw_page():
    img = Image.new("RGB", (W, 1400), PAPER)
    d = ImageDraw.Draw(img)
    y = 36

    # Masthead
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, y), title, font=F_TITLE, fill=INK)
    y += 60
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RED, width=4)
    y += 12
    date = "WEDNESDAY, 25 NOVEMBER 2026  •  SUM UP OF THE DAY'S WORLD NEWS"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, y), date, font=F_DATE, fill=MUTED)
    y += 26
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    y += 18

    # Lead story
    d.text((MARGIN, y), LEAD["label"], font=F_LABEL, fill=RED)
    y += 26
    lines = wrap(d, LEAD["headline"], F_HEAD, CONTENT_W)
    y = text_block(d, MARGIN, y, lines, F_HEAD, INK, 40)
    y += 4
    lines = wrap(d, LEAD["body"], F_BODY, CONTENT_W)
    y = text_block(d, MARGIN, y, lines, F_BODY, INK, 26)
    y += 14
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 14

    # Two-column grid of stories
    col_w = (CONTENT_W - 24) // 2
    for row in range(0, len(STORIES), 2):
        pair = STORIES[row:row + 2]
        heights = []
        for s in pair:
            hl = wrap(d, s["headline"], F_HEAD_SM, col_w)
            bl = wrap(d, s["body"], F_BODY_SM, col_w)
            heights.append(26 + len(hl) * 30 + 5 + len(bl) * 24)
        row_h = max(heights)
        for i, s in enumerate(pair):
            x = MARGIN + i * (col_w + 24)
            cy = y
            d.text((x, cy), s["label"], font=F_LABEL, fill=s["color"])
            cy += 26
            hl = wrap(d, s["headline"], F_HEAD_SM, col_w)
            cy = text_block(d, x, cy, hl, F_HEAD_SM, INK, 30)
            cy += 5
            bl = wrap(d, s["body"], F_BODY_SM, col_w)
            text_block(d, x, cy, bl, F_BODY_SM, INK, 24)
        y += row_h + 12
        d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
        y += 12

    # Also today
    d.text((MARGIN, y), "ALSO TODAY", font=F_LABEL, fill=MUTED)
    y += 26
    lines = wrap(d, ALSO, F_BODY_SM, CONTENT_W)
    y = text_block(d, MARGIN, y, lines, F_BODY_SM, INK, 24)
    y += 18

    # Footer
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 10
    foot = ("Sources: Reuters, AP, AFP, Al Jazeera, Just Security.  •  "
            "Built by an AI agent for make.fun")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, y), foot, font=F_FOOT, fill=MUTED)
    y += 28

    img = img.crop((0, 0, W, y + 24))
    img.save(OUT, "PNG")
    print(f"Wrote {OUT} ({img.size[0]}x{img.size[1]}, "
          f"{os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    draw_page()
