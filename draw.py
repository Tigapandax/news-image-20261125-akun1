"""Paint the one-page news poster for Wednesday 25 November 2026.

Build-time helper only: run this once to produce ``entry.png``. The
competition entry itself is shipped by ``main.py`` (stdlib only);
this file is the only place Pillow is needed.

Layout, from top to bottom on a deep-navy broadsheet:

* masthead with the date,
* one full-width lead story (the Strait of Hormuz),
* two columns of two story cards each,
* a row of three short items,
* an "also today" ticker and a footer line.
"""

from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1008
EDGE = 36
GAP = 20

NAVY = (15, 29, 50)
PAPER = (246, 240, 228)
PAPER_SOFT = (233, 225, 206)
CRIMSON = (166, 30, 45)
GOLD = (217, 164, 65)
INK = (22, 30, 44)
SLATE = (86, 95, 111)
OFFWHITE = (250, 248, 243)
HAIRLINE = (198, 188, 166)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font_at(name: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a DejaVu face at the requested point size."""
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BOLD = lambda size: font_at("DejaVuSerif-Bold.ttf", size)
SERIF = lambda size: font_at("DejaVuSerif.ttf", size)
SANS = lambda size: font_at("DejaVuSans.ttf", size)
SANS_BOLD = lambda size: font_at("DejaVuSans-Bold.ttf", size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str,
              font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    """Greedy word wrap: split *text* into lines no wider than *width*."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def blurb(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
          font: ImageFont.FreeTypeFont, fill: tuple[int, int, int],
          width: int, leading: int) -> int:
    """Draw *text* wrapped inside *width*; return the y after the block."""
    for line in wrap_text(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def chip(draw: ImageDraw.ImageDraw, x: int, y: int, label: str) -> int:
    """Paint a small crimson label chip; return its right edge."""
    font = SANS_BOLD(15)
    pad_x, pad_y = 10, 5
    text_w = int(draw.textlength(label, font=font))
    box_h = 15 + pad_y * 2
    draw.rounded_rectangle(
        [x, y, x + text_w + pad_x * 2, y + box_h],
        radius=4, fill=CRIMSON,
    )
    draw.text((x + pad_x, y + pad_y), label, font=font, fill=OFFWHITE)
    return x + text_w + pad_x * 2


def hairline(draw: ImageDraw.ImageDraw, y: int, x0: int, x1: int,
             fill: tuple[int, int, int] = HAIRLINE, width: int = 2) -> None:
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def masthead(draw: ImageDraw.ImageDraw) -> int:
    """Top of the page: gold rule, title, date line, thin rule."""
    y = 26
    draw.line([(EDGE, y), (PAGE_W - EDGE, y)], fill=GOLD, width=5)
    y += 18
    title = "THE WORLD IN ONE PICTURE"
    title_font = SERIF_BOLD(52)
    title_w = int(draw.textlength(title, font=title_font))
    draw.text(((PAGE_W - title_w) // 2, y), title,
              font=title_font, fill=OFFWHITE)
    y += 66
    dateline = "WEDNESDAY, 25 NOVEMBER 2026  •  ONE DAY, ONE PLANET"
    date_font = SANS(19)
    date_w = int(draw.textlength(dateline, font=date_font))
    draw.text(((PAGE_W - date_w) // 2, y), dateline,
              font=date_font, fill=GOLD)
    y += 34
    hairline(draw, y, EDGE, PAGE_W - EDGE, fill=GOLD, width=2)
    return y + 16


def lead_story(draw: ImageDraw.ImageDraw, y: int) -> int:
    """Full-width lead panel: the Hormuz tanker attacks."""
    top = y
    height = 196
    draw.rounded_rectangle(
        [EDGE, top, PAGE_W - EDGE, top + height],
        radius=10, fill=PAPER,
    )
    pad = 26
    inner_w = PAGE_W - 2 * EDGE - 2 * pad
    x = EDGE + pad
    cy = top + 20
    chip(draw, x, cy, "LEAD  •  STRAIT OF HORMUZ")
    cy += 42
    headline = "Mines set two tankers ablaze in the Strait of Hormuz"
    cy = blurb(draw, x, cy, headline, SERIF_BOLD(38), INK, inner_w, 44)
    deck = ("Houthi rebels say they also struck the Ras Tanura refinery "
            "on Saudi Arabia's Gulf coast.")
    blurb(draw, x, cy + 4, deck, SANS(20), SLATE, inner_w, 27)
    return top + height


def story_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int],
               kicker: str, headline: str, deck: str) -> None:
    """One paper card: crimson kicker, serif headline, short deck."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=PAPER)
    pad = 20
    inner_w = (x1 - x0) - 2 * pad
    x = x0 + pad
    y = y0 + 16
    draw.text((x, y), kicker, font=SANS_BOLD(15), fill=CRIMSON)
    y += 26
    y = blurb(draw, x, y, headline, SERIF_BOLD(24), INK, inner_w, 30)
    blurb(draw, x, y + 6, deck, SANS(17), SLATE, inner_w, 23)


def mini_item(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int],
              kicker: str, text: str) -> None:
    """A compact paper tile for a shorter story."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=PAPER_SOFT)
    pad = 18
    inner_w = (x1 - x0) - 2 * pad
    x = x0 + pad
    y = y0 + 14
    draw.text((x, y), kicker, font=SANS_BOLD(14), fill=CRIMSON)
    y += 24
    blurb(draw, x, y, text, SERIF_BOLD(19), INK, inner_w, 25)


def ticker_strip(draw: ImageDraw.ImageDraw, y: int) -> int:
    """Gold-outlined strip with the day's remaining headlines."""
    top = y
    height = 84
    draw.rounded_rectangle(
        [EDGE, top, PAGE_W - EDGE, top + height],
        radius=8, outline=GOLD, width=2,
    )
    label = "ALSO TODAY  —  "
    font = SANS_BOLD(17)
    x = EDGE + 18
    draw.text((x, top + 16), label, font=font, fill=GOLD)
    x += int(draw.textlength(label, font=font))
    items = ("Shenzhou-24 docks with Tiangong  •  Cartagena supermarket "
             "hostages freed  •  Bogor mine toll reaches six  •  Macy's "
             "parade delayed by storm")
    blurb(draw, x, top + 16, items, SANS(17), OFFWHITE,
          PAGE_W - EDGE - 18 - x, 22)
    return top + height


def footer_note(draw: ImageDraw.ImageDraw, y: int) -> None:
    """Small centred credit line at the very bottom."""
    note = "Painted by an AI agent from public news wires  •  25 November 2026"
    font = SANS(15)
    note_w = int(draw.textlength(note, font=font))
    draw.text(((PAGE_W - note_w) // 2, y), note, font=font, fill=SLATE)


def build_poster() -> Image.Image:
    """Compose every section onto one navy broadsheet page."""
    page = Image.new("RGB", (PAGE_W, PAGE_H), NAVY)
    draw = ImageDraw.Draw(page)

    y = masthead(draw)
    y = lead_story(draw, y)
    y += GAP

    col_w = (PAGE_W - 2 * EDGE - GAP) // 2
    left_x = EDGE
    right_x = EDGE + col_w + GAP
    card_h = 140
    row_gap = 14

    story_card(draw, (left_x, y, left_x + col_w, y + card_h),
               "UKRAINE  •  WAR",
               "Ukrainian drones set two Rosneft refineries on fire",
               "Syzran, Kuibyshev hit; two dead in Odesa.")
    story_card(draw, (left_x, y + card_h + row_gap,
                      left_x + col_w, y + 2 * card_h + row_gap),
               "TECH  •  BROOKLYN",
               "Huawei found guilty on 10 of 12 counts",
               "A US jury convicts the Chinese tech giant.")
    story_card(draw, (right_x, y, right_x + col_w, y + card_h),
               "MARKETS",
               "Asia slides as the Dow crosses 50,000",
               "KOSPI −6.2%, Nikkei −2.8%; Dow tops 50,000.")
    story_card(draw, (right_x, y + card_h + row_gap,
                      right_x + col_w, y + 2 * card_h + row_gap),
               "EGYPT",
               "Fuel tanker fire near Cairo kills at least 31",
               "Blaze engulfs a fuel tanker by the capital.")
    y += 2 * card_h + row_gap + GAP

    tile_w = (PAGE_W - 2 * EDGE - 2 * GAP) // 3
    tile_h = 148
    mini_item(draw, (EDGE, y, EDGE + tile_w, y + tile_h),
              "SUDAN",
              "RSF drone strike kills 19 civilians")
    mini_item(draw, (EDGE + tile_w + GAP, y,
                     EDGE + 2 * tile_w + GAP, y + tile_h),
              "CLIMATE  •  COP31",
              "Pope laments COP31 failure; Australia–Solomon Islands "
              "treaty signed")
    mini_item(draw, (EDGE + 2 * tile_w + 2 * GAP, y,
                     PAGE_W - EDGE, y + tile_h),
              "RIYADH",
              "Houthi drone attack on a tower wounds 11")
    y += tile_h + GAP

    y = ticker_strip(draw, y)
    footer_note(draw, y + 18)
    return page


if __name__ == "__main__":
    poster = build_poster()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "entry.png")
    poster.save(out_path, format="PNG", optimize=True)
    size = os.path.getsize(out_path)
    print(f"poster saved: {out_path} "
          f"({poster.width}x{poster.height}, {size} bytes)")
