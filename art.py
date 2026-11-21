"""art.py - Auralis passport artwork: guilloche, emblem, portrait, MRZ, stamps.

Pure Python 3 standard library only. Imports Canvas from pngcore and
draw_text / text_width from font.
"""

import math

from pngcore import Canvas
from font import draw_text, text_width


# ---------- guilloche ----------

def guilloche(canvas, x, y, w, h, color, step=7):
    """Fine guilloche: thin concentric arcs / sine-wave lines clipped to rect."""
    cx = x + w / 2.0
    cy = y + h / 2.0
    # concentric arcs
    r = 4.0
    while r < math.hypot(w, h) / 2.0:
        _arc(canvas, cx, cy, r, color, x, y, w, h)
        r += step
    # diagonal sine-wave family, clipped to the rect
    for k in range(-int(h / step) - 1, int(w / step) + 1):
        base = x + k * step
        prev = None
        for yy in range(y, y + h, 2):
            xx = base + (yy - y) * 0.35 + math.sin((yy - y) / 6.0) * 2.0
            if x <= xx <= x + w:
                if prev is not None:
                    canvas.line(prev[0], prev[1], xx, yy, color, 1)
                prev = (xx, yy)
            else:
                prev = None


def _arc(canvas, cx, cy, r, color, x, y, w, h):
    steps = max(24, int(2 * math.pi * r))
    prev = None
    for s in range(steps + 1):
        a = 2 * math.pi * s / steps
        px = cx + r * math.cos(a)
        py = cy + r * math.sin(a)
        if x <= px <= x + w and y <= py <= y + h:
            if prev is not None:
                canvas.line(prev[0], prev[1], px, py, color, 1)
            prev = (px, py)
        else:
            prev = None


# ---------- emblem ----------

def draw_emblem(canvas, cx, cy, r, ink, accent):
    """Auralis coat of arms: round seal with aurora, mountain, wave, star."""
    # outer ring
    canvas.circle(cx, cy, r, ink, fill=False)
    canvas.circle(cx, cy, r * 0.92, ink, fill=False)
    # inner field
    canvas.circle(cx, cy, r * 0.88, ink, fill=True)
    # aurora: three wavy bands
    for i, off in enumerate((-0.18, 0.0, 0.18)):
        _wavy_band(canvas, cx, cy, r, off, accent, i)
    # mountain triangle
    m = r * 0.42
    canvas.poly([(cx - m, cy + m * 0.55), (cx, cy - m * 0.45),
                 (cx + m, cy + m * 0.55)], accent)
    # wave line at base
    yw = cy + m * 0.62
    for k in range(-int(r), int(r), 4):
        canvas.line(cx + k, yw, cx + k + 2, yw, accent, 1)
    # small star above
    _star(canvas, cx, cy - r * 0.72, r * 0.16, accent)


def _wavy_band(canvas, cx, cy, r, off, color, phase):
    x0 = cx - r * 0.75
    x1 = cx + r * 0.75
    steps = 24
    prev = None
    for s in range(steps + 1):
        t = s / steps
        xx = x0 + (x1 - x0) * t
        yy = cy + off * r + math.sin(t * math.pi * 3 + phase) * r * 0.10
        if prev is not None:
            canvas.line(prev[0], prev[1], xx, yy, color, 1)
        prev = (xx, yy)


def _star(canvas, cx, cy, r, color):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    canvas.poly(pts, color)


# ---------- portrait ----------

def draw_portrait(canvas, x, y, w, h):
    """Flat-illustration passport portrait of Freya Anette Solberg."""
    skin = (222, 190, 168)
    skin_sh = (205, 172, 150)
    hair = (96, 88, 82)
    navy = (36, 52, 74)
    collar = (222, 226, 232)
    bg = (168, 182, 196)
    ink = (40, 40, 40)

    # background
    canvas.fill_rect(x, y, w, h, bg)
    guilloche(canvas, x, y, w, h, (150, 164, 178), step=9)

    cx = x + w / 2.0

    # shoulders / jacket
    sh_y = y + h * 0.72
    canvas.poly([(x + 2, y + h - 2), (x + w - 2, y + h - 2),
                 (x + w * 0.78, sh_y), (x + w * 0.22, sh_y)], navy)
    # collar
    canvas.poly([(cx - w * 0.14, sh_y), (cx, sh_y + h * 0.10),
                 (cx + w * 0.14, sh_y)], collar)

    # neck
    canvas.fill_rect(int(cx - w * 0.07), int(sh_y - h * 0.06),
                     int(w * 0.14), int(h * 0.12), skin)

    # face oval
    face_cx = cx
    face_cy = y + h * 0.40
    face_rx = w * 0.26
    face_ry = h * 0.30
    canvas.ellipse(face_cx, face_cy, face_rx, face_ry, skin, fill=True)

    # hair: dark ash-blonde bob framing the face
    canvas.ellipse(face_cx, face_cy - h * 0.04, face_rx * 1.22, face_ry * 1.18,
                   hair, fill=True)
    # cut away lower hair to reveal face
    canvas.ellipse(face_cx, face_cy + h * 0.02, face_rx * 0.94, face_ry * 0.98,
                   skin, fill=True)
    # hair sides (bob)
    canvas.fill_rect(int(face_cx - face_rx * 1.22), int(face_cy - h * 0.10),
                     int(face_rx * 0.30), int(face_ry * 1.6), hair)
    canvas.fill_rect(int(face_cx + face_rx * 0.92), int(face_cy - h * 0.10),
                     int(face_rx * 0.30), int(face_ry * 1.6), hair)

    # features
    ey = face_cy - h * 0.02
    ex = face_rx * 0.42
    # eyes
    canvas.line(face_cx - ex - 3, ey, face_cx - ex + 3, ey, ink, 1)
    canvas.line(face_cx + ex - 3, ey, face_cx + ex + 3, ey, ink, 1)
    # brows
    canvas.line(face_cx - ex - 4, ey - 4, face_cx - ex + 3, ey - 5, ink, 1)
    canvas.line(face_cx + ex - 3, ey - 5, face_cx + ex + 4, ey - 4, ink, 1)
    # nose
    canvas.line(face_cx, ey + 2, face_cx, ey + 8, ink, 1)
    # mouth
    canvas.line(face_cx - 5, face_cy + h * 0.10, face_cx + 5, face_cy + h * 0.10,
                ink, 1)


# ---------- MRZ ----------

def mrz_check(s):
    """ICAO 9303 check digit. '<'=0, '0'-'9'=0-9, 'A'-'Z'=10-35."""
    weights = (7, 3, 1)
    total = 0
    for i, ch in enumerate(s):
        if ch == '<':
            v = 0
        elif ch.isdigit():
            v = ord(ch) - ord('0')
        else:
            v = ord(ch) - ord('A') + 10
        total += v * weights[i % 3]
    return str(total % 10)


def mrz_lines(surname, given, number, nationality, birth, sex, expiry):
    """Two 44-char TD3 MRZ lines with correct ICAO check digits."""
    def clean(s):
        return s.upper().replace(' ', '<')

    line1 = 'P<' + nationality + clean(surname) + '<<' + clean(given)
    line1 = line1.ljust(44, '<')

    num = number.ljust(9, '<')
    num_c = mrz_check(num)
    birth_c = mrz_check(birth)
    expiry_c = mrz_check(expiry)
    personal = '<' * 14
    personal_c = mrz_check(personal)

    line2 = (num + num_c + nationality + birth + birth_c + sex +
             expiry + expiry_c + personal + personal_c)

    # composite check digit over line-2 chars 1-10, 14-20, 22-43 (1-indexed)
    comp_src = line2[0:10] + line2[13:20] + line2[21:43]
    comp = mrz_check(comp_src)
    line2 = line2 + comp

    assert len(line1) == 44, "line1 len %d" % len(line1)
    assert len(line2) == 44, "line2 len %d" % len(line2)
    return line1, line2


# ---------- stamps ----------

def draw_stamp(canvas, cx, cy, r, lines, color, angle_deg=0):
    """Round stamp: two concentric circles, stacked centred small text."""
    canvas.circle(cx, cy, r, color, fill=False)
    canvas.circle(cx, cy, r * 0.88, color, fill=False)
    # small star at top
    _star(canvas, cx, cy - r * 0.72, r * 0.10, color)
    n = len(lines)
    if n == 0:
        return
    longest = max(lines, key=len)
    max_w = r * 1.7
    scale = min(r / 34.0, max_w / (len(longest) * 11.0))
    line_h = 14 * scale * 1.3
    start = cy - (n - 1) * line_h / 2.0
    for i, ln in enumerate(lines):
        draw_text(canvas, ln, cx, start + i * line_h, scale, color,
                  align="center")


def draw_stamp_rect(canvas, x, y, w, h, lines, color):
    """Rectangular stamp: double border, first line larger, rest smaller."""
    canvas.rect(x, y, w, h, color, lw=2)
    canvas.rect(x + 3, y + 3, w - 6, h - 6, color, lw=1)
    n = len(lines)
    if n == 0:
        return
    longest = max(lines, key=len)
    scale1 = min(1.6, (w - 16) / (len(longest) * 11.0))
    draw_text(canvas, lines[0], x + w / 2.0, y + 8, scale1, color,
              align="center")
    rest = lines[1:]
    if rest:
        scale2 = min(1.1, (w - 16) / (max(len(l) for l in rest) * 11.0))
        line_h = 14 * scale2 * 1.25
        start = y + 8 + 14 * scale1 + 6
        for i, ln in enumerate(rest):
            draw_text(canvas, ln, x + w / 2.0, start + i * line_h, scale2,
                      color, align="center")


if __name__ == "__main__":
    import hashlib
    c = Canvas(700, 420, (255, 255, 255))
    draw_emblem(c, 120, 120, 70, (18, 63, 60), (176, 141, 60))
    draw_portrait(c, 300, 60, 150, 190)
    draw_stamp(c, 560, 120, 46, ["ARRIVAL", "PORT LIORAN", "22 SEP 2025"],
               (43, 76, 126))
    draw_stamp_rect(c, 60, 300, 220, 90, ["ENTRY VESTMARK", "02 JUN 2024"],
                    (140, 59, 46))
    l1, l2 = mrz_lines("SOLBERG", "FREYA ANETTE", "AU4829137", "AUR",
                       "900512", "F", "340313")
    print("L1", l1, len(l1))
    print("L2", l2, len(l2))
    c.save("/tmp/art-test.png")
    data = open("/tmp/art-test.png", "rb").read()
    print("size", len(data))
    print("sha256", hashlib.sha256(data).hexdigest())