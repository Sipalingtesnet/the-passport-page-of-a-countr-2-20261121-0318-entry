"""font.py - single-stroke vector font (engraver style).

Pure Python 3 standard library only. Imports Canvas from pngcore.

Glyph coordinate space: x in 0..10, y in 0..14, y=0 is TOP of cap height,
y=14 is BASELINE. Each glyph is a list of strokes; each stroke is a list of
(x, y) points.
"""

from pngcore import Canvas

# Each glyph: list of strokes. A stroke is a list of (x, y) points.
FONT = {
    'A': [[(1, 14), (5, 0)], [(9, 14), (5, 0)], [(2.5, 9), (7.5, 9)]],
    'B': [[(2, 0), (2, 14)],
          [(2, 0), (7, 0), (9, 2), (9, 5), (7, 7), (2, 7)],
          [(2, 7), (7, 7), (9, 9), (9, 12), (7, 14), (2, 14)]],
    'C': [[(9, 3), (7, 1), (4, 1), (2, 3), (2, 11), (4, 13), (7, 13), (9, 11)]],
    'D': [[(2, 0), (2, 14)], [(2, 0), (6, 0), (9, 3), (9, 11), (6, 14), (2, 14)]],
    'E': [[(2, 0), (2, 14)], [(2, 0), (9, 0)], [(2, 7), (8, 7)], [(2, 14), (9, 14)]],
    'F': [[(2, 0), (2, 14)], [(2, 0), (9, 0)], [(2, 7), (8, 7)]],
    'G': [[(9, 3), (7, 1), (4, 1), (2, 3), (2, 11), (4, 13), (7, 13), (9, 11),
           (9, 7), (5, 7)]],
    'H': [[(2, 0), (2, 14)], [(8, 0), (8, 14)], [(2, 7), (8, 7)]],
    'I': [[(5, 0), (5, 14)], [(3, 0), (7, 0)], [(3, 14), (7, 14)]],
    'J': [[(8, 0), (8, 11), (6, 13), (4, 13), (2, 11)], [(3, 0), (7, 0)]],
    'K': [[(2, 0), (2, 14)], [(8, 0), (2, 7)], [(2, 7), (8, 14)]],
    'L': [[(2, 0), (2, 14)], [(2, 14), (9, 14)]],
    'M': [[(1, 14), (1, 0), (5, 8), (9, 0), (9, 14)]],
    'N': [[(2, 14), (2, 0), (8, 14), (8, 0)]],
    'O': [[(5, 1), (2, 3), (2, 11), (5, 13), (8, 11), (8, 3), (5, 1)]],
    'P': [[(2, 0), (2, 14)],
          [(2, 0), (7, 0), (9, 2), (9, 5), (7, 7), (2, 7)]],
    'Q': [[(5, 1), (2, 3), (2, 11), (5, 13), (8, 11), (8, 3), (5, 1)],
          [(6, 10), (9, 14)]],
    'R': [[(2, 0), (2, 14)],
          [(2, 0), (7, 0), (9, 2), (9, 5), (7, 7), (2, 7)],
          [(5, 7), (9, 14)]],
    'S': [[(9, 2), (7, 0), (3, 0), (2, 2), (2, 5), (8, 9), (8, 12), (6, 14),
           (2, 14)]],
    'T': [[(5, 0), (5, 14)], [(1, 0), (9, 0)]],
    'U': [[(2, 0), (2, 11), (4, 13), (6, 13), (8, 11), (8, 0)]],
    'V': [[(1, 0), (5, 14), (9, 0)]],
    'W': [[(1, 0), (3, 14), (5, 6), (7, 14), (9, 0)]],
    'X': [[(1, 0), (9, 14)], [(9, 0), (1, 14)]],
    'Y': [[(1, 0), (5, 7), (9, 0)], [(5, 7), (5, 14)]],
    'Z': [[(1, 0), (9, 0), (1, 14), (9, 14)]],
    '0': [[(5, 1), (2, 3), (2, 11), (5, 13), (8, 11), (8, 3), (5, 1)]],
    '1': [[(4, 2), (5, 0), (5, 14)], [(3, 14), (7, 14)]],
    '2': [[(2, 3), (4, 1), (7, 1), (9, 3), (9, 6), (2, 14), (9, 14)]],
    '3': [[(2, 2), (4, 0), (7, 0), (9, 2), (9, 5), (7, 7), (9, 9), (9, 12),
           (7, 14), (4, 14), (2, 12)]],
    '4': [[(7, 0), (7, 14)], [(2, 4), (2, 6), (7, 11)], [(2, 14), (9, 14)]],
    '5': [[(9, 0), (2, 0), (2, 6), (8, 6), (9, 8), (9, 12), (7, 14), (3, 14),
           (2, 12)]],
    '6': [[(9, 3), (7, 1), (4, 1), (2, 3), (2, 11), (4, 13), (7, 13), (9, 11),
           (9, 8), (2, 8)]],
    '7': [[(2, 0), (9, 0), (5, 14)]],
    '8': [[(5, 1), (2, 3), (2, 5), (5, 7), (8, 5), (8, 3), (5, 1)],
          [(5, 7), (2, 9), (2, 12), (5, 14), (8, 12), (8, 9), (5, 7)]],
    '9': [[(2, 11), (4, 13), (7, 13), (9, 11), (9, 3), (7, 1), (4, 1),
           (2, 3), (2, 6), (9, 6)]],
    ' ': [],
    '.': [[(4.8, 13), (5.2, 13)]],
    ',': [[(5, 13), (4, 14)]],
    '-': [[(2, 7), (8, 7)]],
    '/': [[(2, 14), (8, 0)]],
    ':': [[(4.8, 4), (5.2, 4)], [(4.8, 10), (5.2, 10)]],
    '(': [[(7, 2), (5, 4), (5, 10), (7, 12)]],
    ')': [[(3, 2), (5, 4), (5, 10), (3, 12)]],
    "'": [[(5, 2), (5, 5)]],
    '&': [[(8, 2), (6, 0), (3, 0), (2, 2), (2, 4), (8, 10), (8, 12), (6, 14),
           (3, 14), (2, 12)], [(2, 4), (3, 6), (6, 6), (8, 8)]],
    '+': [[(5, 2), (5, 12)], [(1, 7), (9, 7)]],
    '%': [[(2, 2), (2, 2)], [(8, 12), (8, 12)], [(2, 2), (8, 12)],
          [(2, 12), (2, 12)], [(8, 2), (8, 2)]],
    '!': [[(5, 0), (5, 10)], [(4.8, 13), (5.2, 13)]],
    '?': [[(2, 2), (4, 0), (7, 0), (9, 2), (9, 5), (5, 8), (5, 11)],
          [(4.8, 13), (5.2, 13)]],
    '=': [[(2, 5), (8, 5)], [(2, 9), (8, 9)]],
    '<': [[(8, 2), (2, 7), (8, 12)]],
}


def _glyph(ch):
    if ch in FONT:
        return FONT[ch]
    up = ch.upper()
    if up in FONT:
        return FONT[up]
    return None


def text_width(text, scale, spacing=1.0):
    """Advance width in px. Each char advances (10 + spacing) * scale."""
    return len(text) * (10 + spacing) * scale


def draw_text(canvas, text, x, y, scale, color, align="left", spacing=1.0,
              lw=None):
    """Draw text with top of cap at pixel y. Returns drawn width in px."""
    if lw is None:
        lw = max(1, round(scale * 0.22))
    adv = (10 + spacing) * scale
    total = len(text) * adv
    if align == "center":
        x = x - total / 2.0
    elif align == "right":
        x = x - total
    cx = x
    for ch in text:
        g = _glyph(ch)
        if g is not None:
            for stroke in g:
                pts = [(cx + p[0] * scale, y + p[1] * scale) for p in stroke]
                for i in range(len(pts) - 1):
                    canvas.line(pts[i][0], pts[i][1],
                                pts[i + 1][0], pts[i + 1][1], color, lw)
        cx += adv
    return total


def draw_text_wrapped(canvas, text, x, y, max_w, scale, color, line_gap=0.35,
                      align="left", spacing=1.0):
    """Word-wrap text to max_w px. Returns y just below the last line."""
    adv = (10 + spacing) * scale
    line_h = 14 * scale * (1 + line_gap)
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) * adv <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    yy = y
    for ln in lines:
        draw_text(canvas, ln, x, yy, scale, color, align=align, spacing=spacing)
        yy += line_h
    return yy


if __name__ == "__main__":
    import hashlib
    c = Canvas(900, 220, (255, 255, 255))
    draw_text(c, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 20, 20, 2, (20, 20, 20))
    draw_text(c, "0123456789", 20, 60, 2, (20, 20, 20))
    draw_text(c, "REPUBLIC OF AURALIS - PASSPORT AU-4829137", 20, 100, 3,
              (20, 20, 20))
    draw_text(c, "AURALIS", 20, 150, 5, (20, 20, 20))
    draw_text_wrapped(c, "THE HOLDER MAY LAND ON THE OUTER ISLES ONLY "
                         "BETWEEN 01 NOV AND 28 FEB. MAINLAND TRANSIT "
                         "PROHIBITED.", 20, 170, 700, 2, (20, 20, 20))
    c.save("/tmp/font-test.png")
    data = open("/tmp/font-test.png", "rb").read()
    print("size", len(data))
    print("sha256", hashlib.sha256(data).hexdigest())