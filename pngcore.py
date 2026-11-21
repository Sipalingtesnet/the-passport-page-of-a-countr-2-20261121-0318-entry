"""pngcore.py - minimal deterministic PNG writer and Canvas drawing primitives.

Pure Python 3 standard library only (struct, zlib, math). No Pillow.
"""

import struct
import zlib
import math


def clamp(v, lo, hi):
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


def lerp(a, b, t):
    return a + (b - a) * t


def save_png(path, w, h, px):
    """Write a true-colour RGB PNG (colour type 2, bit depth 8, no interlace).

    px is a flat bytearray of length w*h*3 (row-major RGB). zlib level 9,
    filter byte 0 per scanline. Deterministic.
    """
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        c += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return c

    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw.append(0)  # filter type 0
        raw += px[y * stride:(y + 1) * stride]

    comp = zlib.compress(bytes(raw), 9)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    out = sig
    out += chunk(b"IHDR", ihdr)
    out += chunk(b"IDAT", comp)
    out += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(out)


class Canvas:
    """Row-major RGB canvas with safe, clipped drawing primitives."""

    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        r, g, b = bg
        for i in range(0, len(self.px), 3):
            self.px[i] = r
            self.px[i + 1] = g
            self.px[i + 2] = b

    def _idx(self, x, y):
        return (y * self.w + x) * 3

    def set(self, x, y, c):
        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return
        i = self._idx(x, y)
        self.px[i] = c[0]
        self.px[i + 1] = c[1]
        self.px[i + 2] = c[2]

    def get(self, x, y):
        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return (0, 0, 0)
        i = self._idx(x, y)
        return (self.px[i], self.px[i + 1], self.px[i + 2])

    def fill_rect(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            i = self._idx(x0, yy)
            for xx in range(x0, x1):
                self.px[i] = c[0]
                self.px[i + 1] = c[1]
                self.px[i + 2] = c[2]
                i += 3

    def rect(self, x, y, w, h, c, lw=1):
        for k in range(lw):
            self.line(x + k, y + k, x + w - 1 - k, y + k, c, 1)
            self.line(x + k, y + h - 1 - k, x + w - 1 - k, y + h - 1 - k, c, 1)
            self.line(x + k, y + k, x + k, y + h - 1 - k, c, 1)
            self.line(x + w - 1 - k, y + k, x + w - 1 - k, y + h - 1 - k, c, 1)

    def line(self, x0, y0, x1, y1, c, lw=1):
        if lw <= 1:
            self._line1(x0, y0, x1, y1, c)
        else:
            dx = x1 - x0
            dy = y1 - y0
            dist = math.hypot(dx, dy)
            steps = max(1, int(dist))
            r = (lw - 1) / 2.0
            for s in range(steps + 1):
                t = s / steps
                px = x0 + dx * t
                py = y0 + dy * t
                self._disc(px, py, r, c)

    def _line1(self, x0, y0, x1, y1, c):
        x0 = int(round(x0))
        y0 = int(round(y0))
        x1 = int(round(x1))
        y1 = int(round(y1))
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def _disc(self, cx, cy, r, c):
        x0 = int(math.floor(cx - r))
        x1 = int(math.ceil(cx + r))
        y0 = int(math.floor(cy - r))
        y1 = int(math.ceil(cy + r))
        r2 = r * r
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r2:
                    self.set(xx, yy, c)

    def circle(self, cx, cy, r, c, fill=True):
        if fill:
            self._disc(cx, cy, r, c)
        else:
            self._ring(cx, cy, r, c)

    def _ring(self, cx, cy, r, c):
        steps = max(24, int(2 * math.pi * r))
        for s in range(steps):
            a = 2 * math.pi * s / steps
            x = cx + r * math.cos(a)
            y = cy + r * math.sin(a)
            self.set(int(round(x)), int(round(y)), c)

    def ellipse(self, cx, cy, rx, ry, c, fill=True):
        steps = max(32, int(2 * math.pi * max(rx, ry)))
        if fill:
            for yy in range(int(math.floor(cy - ry)), int(math.ceil(cy + ry)) + 1):
                for xx in range(int(math.floor(cx - rx)), int(math.ceil(cx + rx)) + 1):
                    if ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0:
                        self.set(xx, yy, c)
        else:
            for s in range(steps):
                a = 2 * math.pi * s / steps
                x = cx + rx * math.cos(a)
                y = cy + ry * math.sin(a)
                self.set(int(round(x)), int(round(y)), c)

    def poly(self, points, c):
        """Filled polygon, scanline fill. Works for convex and simple concave."""
        if not points:
            return
        ys = [p[1] for p in points]
        ymin = max(0, int(math.floor(min(ys))))
        ymax = min(self.h - 1, int(math.ceil(max(ys))))
        for y in range(ymin, ymax + 1):
            xs = []
            n = len(points)
            for i in range(n):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % n]
                if (y1 <= y < y2) or (y2 <= y < y1):
                    if y2 != y1:
                        t = (y - y1) / (y2 - y1)
                        xs.append(x1 + t * (x2 - x1))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                xa = max(0, int(math.floor(xs[k])))
                xb = min(self.w - 1, int(math.ceil(xs[k + 1])))
                for xx in range(xa, xb + 1):
                    self.set(xx, y, c)

    def blend(self, x, y, c, a):
        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return
        i = self._idx(x, y)
        r = self.px[i]
        g = self.px[i + 1]
        b = self.px[i + 2]
        self.px[i] = int(round(r + (c[0] - r) * a))
        self.px[i + 1] = int(round(g + (c[1] - g) * a))
        self.px[i + 2] = int(round(b + (c[2] - b) * a))

    def save(self, path):
        save_png(path, self.w, self.h, self.px)


if __name__ == "__main__":
    import hashlib
    c = Canvas(200, 120, (255, 255, 255))
    c.fill_rect(10, 10, 60, 40, (200, 30, 30))
    c.rect(80, 10, 60, 40, (30, 30, 200), lw=3)
    c.line(10, 100, 190, 20, (30, 200, 30), lw=5)
    c.circle(150, 90, 22, (200, 200, 30), fill=True)
    c.ellipse(50, 90, 30, 14, (200, 30, 200), fill=False)
    c.poly([(100, 60), (130, 90), (100, 110), (70, 90)], (30, 30, 200))
    c.save("/tmp/pngcore-test.png")
    data = open("/tmp/pngcore-test.png", "rb").read()
    print("size", len(data))
    print("sha256", hashlib.sha256(data).hexdigest())
    print("sig", data[:8])