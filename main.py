"""main.py - REPUBLIC OF AURALIS passport spread (invented country).

Pure Python 3 standard library only. Renders a 1024x724 open passport spread
to entry.png in $MAKEFUN_OUTPUT_DIR or /output. Deterministic.
"""

import os
import hashlib

from pngcore import Canvas
from font import draw_text, text_width, draw_text_wrapped
from art import (guilloche, draw_emblem, draw_portrait, mrz_lines,
                 draw_stamp, draw_stamp_rect)

# palette
CREAM = (246, 239, 221)
INK = (18, 63, 60)          # deep teal
GOLD = (176, 141, 60)
STAMP_BLUE = (43, 76, 126)
STAMP_RED = (140, 59, 46)
NEAR_BLACK = (28, 26, 22)
WHITE = (255, 255, 255)

W = 1024
H = 724


def _field(c, x, y, label, value, vscale=1.3):
    draw_text(c, label, x, y, 1.0, INK)
    draw_text(c, value, x, y + 18, vscale, NEAR_BLACK)


def draw_left_page(c):
    """Data page."""
    # header band
    c.fill_rect(28, 28, 472, 68, INK)
    draw_text(c, "REPUBLIC OF AURALIS", 264, 38, 1.6, WHITE, align="center")
    draw_text(c, "PASSPORT", 264, 72, 1.2, WHITE, align="center")
    # small emblem top-right of page
    draw_emblem(c, 472, 62, 22, GOLD, GOLD)

    # photo box
    px, py, pw, ph = 40, 110, 150, 190
    c.rect(px, py, pw, ph, INK, lw=2)
    guilloche(c, px + 3, py + 3, pw - 6, ph - 6, (200, 200, 190), step=8)
    draw_portrait(c, px + 3, py + 3, pw - 6, ph - 6)
    c.rect(px, py, pw, ph, INK, lw=2)
    draw_text(c, "PHOTOGRAPH", px + pw / 2.0, py + ph + 8, 1.0, INK,
              align="center")

    # fields to the right of the photo, single column
    fx = 200
    fields_r = [
        ("SURNAME", "SOLBERG"),
        ("GIVEN NAMES", "FREYA ANETTE"),
        ("NATIONALITY", "AURALIC"),
        ("DATE OF BIRTH", "12 MAY 1990"),
        ("SEX", "F"),
        ("PLACE OF BIRTH", "LIORAN, AURALIS"),
    ]
    for i, (lab, val) in enumerate(fields_r):
        _field(c, fx, 112 + i * 40, lab, val)

    # fields below the photo
    _field(c, 40, 372, "DATE OF ISSUE", "14 MAR 2024")
    _field(c, 40, 412, "DATE OF EXPIRY", "13 MAR 2034")
    _field(c, 40, 452, "AUTHORITY", "MINISTRY OF THE INTERIOR - LIORAN",
           vscale=1.1)
    _field(c, 40, 492, "PASSPORT NO.", "AU 4829137")

    # MRZ strip at bottom
    l1, l2 = mrz_lines("SOLBERG", "FREYA ANETTE", "AU4829137", "AUR",
                       "900512", "F", "340313")
    mrz_y = 640
    c.fill_rect(40, mrz_y - 8, 450, 64, (238, 232, 214))
    c.rect(40, mrz_y - 8, 450, 64, INK, lw=1)
    draw_text(c, l1, 40, mrz_y, 1.0, NEAR_BLACK, spacing=0.1)
    draw_text(c, l2, 40, mrz_y + 30, 1.0, NEAR_BLACK, spacing=0.1)


def draw_right_page(c):
    """Visas / stamps page."""
    # heading
    draw_text(c, "VISAS", 760, 44, 2.0, INK, align="center")
    draw_text(c, "ENDORSEMENTS AND ENTRY STAMPS", 760, 76, 1.0, INK,
              align="center")

    # faint large emblem watermark behind stamps
    draw_emblem(c, 760, 400, 150, (200, 195, 180), (200, 195, 180))

    # permit box
    pbx, pby, pbw, pbh = 540, 92, 440, 143
    c.rect(pbx, pby, pbw, pbh, INK, lw=2)
    c.rect(pbx + 3, pby + 3, pbw - 6, pbh - 6, INK, lw=1)
    draw_text(c, "OUTER ISLES PERMIT", pbx + pbw / 2.0, pby + 10, 1.5, INK,
              align="center")
    draw_text_wrapped(c,
                      "THE HOLDER MAY LAND ON THE OUTER ISLES ONLY BETWEEN "
                      "01 NOV AND 28 FEB. MAINLAND TRANSIT PROHIBITED. - "
                      "HARBOUR MASTER, LIORAN",
                      pbx + 14, pby + 40, pbw - 28, 0.9, NEAR_BLACK)
    # fee stamp
    draw_stamp_rect(c, pbx + pbw - 190, pby + pbh - 30, 180, 22,
                    ["FERRY LEVY PAID 12 KOR"], STAMP_RED)

    # five stamps, two rows
    # row 1
    draw_stamp_rect(c, 535, 255, 145, 84, ["ENTRY VESTMARK", "02 JUN 2024"],
                    STAMP_BLUE)
    draw_stamp_rect(c, 685, 255, 145, 84, ["EXIT VESTMARK", "18 JUN 2024"],
                    STAMP_RED)
    draw_stamp_rect(c, 835, 255, 145, 84, ["ENTRY THALASSA", "09 SEP 2025"],
                    STAMP_BLUE)
    # row 2
    draw_stamp_rect(c, 560, 400, 150, 84, ["EXIT THALASSA", "21 SEP 2025"],
                    STAMP_RED)
    draw_stamp(c, 830, 442, 50, ["ARRIVAL", "PORT LIORAN", "22 SEP 2025"],
               STAMP_BLUE)


def main():
    c = Canvas(W, H, CREAM)

    # outer double border around the whole spread
    c.rect(14, 14, W - 28, H - 28, INK, lw=3)
    c.rect(20, 20, W - 40, H - 40, INK, lw=1)

    # centre gutter fold line
    c.line(512, 28, 512, 696, INK, lw=1)

    # inner rule framing each page
    c.rect(28, 28, 472, 668, INK, lw=1)
    c.rect(524, 28, 472, 668, INK, lw=1)

    draw_left_page(c)
    draw_right_page(c)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    c.save(path)
    data = open(path, "rb").read()
    print("entry.png %d sha256 %s" % (len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()