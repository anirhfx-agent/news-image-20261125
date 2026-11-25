#!/usr/bin/env python3
"""The World in One Page - Wednesday 25 November 2026.

Draws one 1024x1024 newspaper front page summarising 25 November 2026
world news. Python 3 standard library only, no network. Deterministic:
two runs produce byte-identical output.

Writes exactly one file, entry.png, to $MAKEFUN_OUTPUT_DIR
(default /output/entry.png).
"""
import os
import struct
import zlib

W = 1024
H = 1024

# ------------------------------------------------------------------ font
# 5x7 bitmap font, drawn from scratch for this entry. Each glyph is
# 7 rows of 5 cells; '#' is ink, ' ' is blank.
FONT = {
    "A": (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "B": ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    "C": (" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"),
    "D": ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
    "E": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    "F": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    "G": (" ####", "#    ", "#    ", "# ###", "#   #", "#   #", " ### "),
    "H": ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "I": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"),
    "J": ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    "K": ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    "L": ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    "M": ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
    "N": ("#   #", "##  #", "##  #", "# # #", "#  ##", "#  ##", "#   #"),
    "O": (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "P": ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    "Q": (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    "R": ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    "S": (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    "T": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    "U": ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "V": ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "W": ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
    "X": ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    "Y": ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
    "Z": ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    "a": ("     ", "     ", " ### ", "    #", " ####", "#   #", " ####"),
    "b": ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#### "),
    "c": ("     ", "     ", " ####", "#    ", "#    ", "#    ", " ####"),
    "d": ("    #", "    #", " ####", "#   #", "#   #", "#   #", " ####"),
    "e": ("     ", "     ", " ### ", "#   #", "#####", "#    ", " ### "),
    "f": ("  ## ", " #  #", " #   ", "###  ", " #   ", " #   ", " #   "),
    "g": ("     ", " ####", "#   #", "#   #", " ####", "    #", " ### "),
    "h": ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#   #"),
    "i": ("  #  ", "     ", " ##  ", "  #  ", "  #  ", "  #  ", " ### "),
    "j": ("   # ", "     ", "  ## ", "   # ", "   # ", "   # ", "##   "),
    "k": ("#    ", "#    ", "#  # ", "# #  ", "##   ", "# #  ", "#  # "),
    "l": (" ##  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "m": ("     ", "     ", "## # ", "# # #", "# # #", "# # #", "# # #"),
    "n": ("     ", "     ", "#### ", "#   #", "#   #", "#   #", "#   #"),
    "o": ("     ", "     ", " ### ", "#   #", "#   #", "#   #", " ### "),
    "p": ("     ", "     ", "#### ", "#   #", "#   #", "#### ", "#    "),
    "q": ("     ", "     ", " ####", "#   #", "#   #", " ####", "    #"),
    "r": ("     ", "     ", "# ## ", "##  #", "#    ", "#    ", "#    "),
    "s": ("     ", "     ", " ####", "#    ", " ### ", "    #", "#### "),
    "t": (" #   ", " #   ", "###  ", " #   ", " #   ", " #   ", "  ## "),
    "u": ("     ", "     ", "#   #", "#   #", "#   #", "#  ##", " ## #"),
    "v": ("     ", "     ", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "w": ("     ", "     ", "#   #", "# # #", "# # #", "# # #", " # # "),
    "x": ("     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"),
    "y": ("     ", "     ", "#   #", "#   #", "#   #", " ####", " ### "),
    "z": ("     ", "     ", "#####", "   # ", "  #  ", " #   ", "#####"),
    "0": (" ### ", "#  ##", "# # #", "##  #", "#   #", "#   #", " ### "),
    "1": ("  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "2": (" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"),
    "3": ("#### ", "    #", "    #", " ### ", "    #", "    #", "#### "),
    "4": ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    "5": ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    "6": (" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "),
    "7": ("#####", "    #", "   # ", "   # ", "  #  ", "  #  ", "  #  "),
    "8": (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    "9": (" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "),
    " ": ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
    ".": ("     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "),
    ",": ("     ", "     ", "     ", "     ", " ##  ", " ##  ", " #   "),
    ":": ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "),
    ";": ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", " #   "),
    "!": ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
    "?": (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
    "-": ("     ", "     ", "     ", " ### ", "     ", "     ", "     "),
    "\u2014": ("     ", "     ", "     ", "#####", "     ", "     ", "     "),
    "'": ("  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "),
    '"': (" # # ", " # # ", "     ", "     ", "     ", "     ", "     "),
    "(": ("   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "),
    ")": (" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "),
    "%": ("##  #", "## # ", "   # ", "  #  ", " #   ", "# ## ", "#  ##"),
    "/": ("    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "),
    "&": (" ### ", "#   #", "# #  ", " #   ", "# # #", "#  # ", " ## #"),
    "$": ("  #  ", " ####", "# #  ", " ### ", "  # #", "#### ", "  #  "),
    "+": ("     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "),
    "=": ("     ", "     ", "#####", "     ", "#####", "     ", "     "),
    "\u2022": ("     ", "     ", " ##  ", " ##  ", "     ", "     ", "     "),
    "\u00b0": (" ##  ", "#  # ", " ##  ", "     ", "     ", "     ", "     "),
    "[": (" ### ", " #   ", " #   ", " #   ", " #   ", " #   ", " ### "),
    "]": (" ### ", "   # ", "   # ", "   # ", "   # ", "   # ", " ### "),
    "*": ("     ", " # # ", " ### ", "#####", " ### ", " # # ", "     "),
    "<": ("   # ", "  #  ", " #   ", "#    ", " #   ", "  #  ", "   # "),
    ">": (" #   ", "  #  ", "   # ", "    #", "   # ", "  #  ", " #   "),
    "#": (" # # ", " # # ", "#####", " # # ", "#####", " # # ", " # # "),
    "@": (" ### ", "#   #", "# ###", "# # #", "# ###", "#    ", " ### "),
    "~": ("     ", "     ", " ## #", "# ## ", "     ", "     ", "     "),
    "^": ("  #  ", " # # ", "     ", "     ", "     ", "     ", "     "),
    "`": ("  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "),
    "_": ("     ", "     ", "     ", "     ", "     ", "     ", "#####"),
    "\\": ("#    ", "#    ", " #   ", "  #  ", "   # ", "    #", "    #"),
    "{": ("  ## ", " #   ", " #   ", "##   ", " #   ", " #   ", "  ## "),
    "}": ("##   ", "   # ", "   # ", "  ## ", "   # ", "   # ", "##   "),
    "|": ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
}

# ------------------------------------------------------------------ canvas
buf = bytearray(W * H * 3)

PAPER = (250, 246, 236)
INK = (17, 17, 17)
NAVY = (27, 42, 74)
RED = (166, 30, 30)
BLUE = (31, 90, 140)
GRAY = (96, 96, 96)
WHITE = (255, 255, 255)
CARD = (255, 253, 247)
SKY = (176, 204, 226)
SEA = (18, 68, 110)
SEALIGHT = (52, 110, 160)
FLAME1 = (230, 110, 20)
FLAME2 = (245, 180, 30)
SMOKE = (120, 120, 120)
HULL = (35, 35, 40)
SUN = (245, 220, 130)


def fill_rect(x, y, w, h, c):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(c) * (x1 - x0)
    n = (x1 - x0) * 3
    for yy in range(y0, y1):
        i = (yy * W + x0) * 3
        buf[i:i + n] = row


def hline(x, y, w, c, t=1):
    fill_rect(x, y, w, t, c)


def vline(x, y, h, c, t=1):
    fill_rect(x, y, t, h, c)


def outline(x, y, w, h, c, t=1):
    hline(x, y, w, c, t)
    hline(x, y + h - t, w, c, t)
    vline(x, y, h, c, t)
    vline(x + w - t, y, h, c, t)


def circle(cx, cy, r, c):
    for dy in range(-r, r + 1):
        dx = int((r * r - dy * dy) ** 0.5)
        fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, c)


def triangle(x1, y1, x2, y2, x3, y3, c):
    pts = sorted([(x1, y1), (x2, y2), (x3, y3)], key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = pts

    def edge(xa, ya, xb, yb, y):
        if yb == ya:
            return float(xa)
        return xa + (xb - xa) * (y - ya) / (yb - ya)

    for y in range(ay, cy + 1):
        if y < by:
            xa = edge(ax, ay, bx, by, y)
            xb = edge(ax, ay, cx, cy, y)
        else:
            xa = edge(bx, by, cx, cy, y)
            xb = edge(ax, ay, cx, cy, y)
        x0, x1 = int(min(xa, xb)), int(max(xa, xb))
        fill_rect(x0, y, x1 - x0 + 1, 1, c)


# ------------------------------------------------------------------ text
def draw_text(x, y, s, scale, c):
    cx = x
    for ch in s:
        g = FONT.get(ch, FONT["?"])
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == "#":
                    fill_rect(cx + col * scale, y + row * scale, scale, scale, c)
        cx += 6 * scale
    return cx


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_centered(x0, x1, y, s, scale, c):
    w = text_w(s, scale)
    draw_text(x0 + (x1 - x0 - w) // 2, y, s, scale, c)


def wrap(s, max_w, scale):
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if text_w(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_para(x, y, s, max_w, scale, c, lh):
    for ln in wrap(s, max_w, scale):
        draw_text(x, y, ln, scale, c)
        y += lh
    return y


# ------------------------------------------------------------------ png
def _chunk(typ, data):
    return (struct.pack(">I", len(data)) + typ + data +
            struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))


def write_png(path):
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += buf[y * W * 3:(y + 1) * W * 3]
    comp = zlib.compress(bytes(raw), 6)
    data = (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr) +
            _chunk(b"IDAT", comp) + _chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)

# ------------------------------------------------------------------ layout
def draw_masthead():
    draw_centered(0, W, 14, "THE WORLD IN ONE PAGE", 5, NAVY)
    draw_centered(0, W, 58,
                  "WEDNESDAY 25 NOVEMBER 2026  \u2022  20 STORIES  \u2022  ONE IMAGE",
                  2, INK)
    hline(20, 82, 984, NAVY, 3)
    hline(20, 88, 984, NAVY, 1)


def draw_scene(x0, y0, w, h):
    # Sky, sun, clouds.
    fill_rect(x0, y0, w, 88, SKY)
    circle(x0 + w - 54, y0 + 34, 16, SUN)
    circle(x0 + 60, y0 + 34, 18, WHITE)
    circle(x0 + 82, y0 + 30, 22, WHITE)
    circle(x0 + 120, y0 + 54, 14, WHITE)
    circle(x0 + 300, y0 + 26, 12, WHITE)
    # Sea and waves.
    fill_rect(x0, y0 + 88, w, h - 88, SEA)
    for wy in (y0 + 104, y0 + 138, y0 + 176, y0 + 214, y0 + 244):
        for wx in range(x0 + 4, x0 + w - 30, 48):
            hline(wx, wy, 28, SEALIGHT, 2)
    # Background tanker (right), smoke from its funnel.
    fill_rect(x0 + 250, y0 + 139, 160, 22, HULL)
    fill_rect(x0 + 250, y0 + 132, 160, 7, (200, 200, 200))
    fill_rect(x0 + 370, y0 + 114, 34, 20, WHITE)
    fill_rect(x0 + 378, y0 + 104, 18, 12, RED)
    circle(x0 + 387, y0 + 96, 8, SMOKE)
    circle(x0 + 392, y0 + 84, 10, SMOKE)
    circle(x0 + 398, y0 + 72, 12, SMOKE)
    # Foreground tanker (left), burning.
    fill_rect(x0 + 20, y0 + 172, 200, 30, HULL)
    hline(x0 + 20, y0 + 196, 200, RED, 4)
    fill_rect(x0 + 180, y0 + 144, 36, 30, WHITE)
    fill_rect(x0 + 190, y0 + 132, 16, 14, (120, 30, 30))
    # Flames over the foreground tanker.
    triangle(x0 + 60, y0 + 172, x0 + 75, y0 + 119, x0 + 90, y0 + 172, FLAME1)
    triangle(x0 + 85, y0 + 172, x0 + 100, y0 + 109, x0 + 115, y0 + 172, FLAME2)
    triangle(x0 + 110, y0 + 172, x0 + 125, y0 + 124, x0 + 140, y0 + 172, FLAME1)
    triangle(x0 + 135, y0 + 172, x0 + 148, y0 + 140, x0 + 160, y0 + 172, FLAME2)
    # Smoke over the flames.
    circle(x0 + 85, y0 + 104, 10, SMOKE)
    circle(x0 + 100, y0 + 89, 13, SMOKE)
    circle(x0 + 115, y0 + 72, 15, SMOKE)
    # Naval mines in the water.
    for mx, my in ((x0 + 240, y0 + 224), (x0 + 380, y0 + 239),
                   (x0 + 40, y0 + 239), (x0 + 150, y0 + 252)):
        circle(mx, my, 6, (10, 10, 10))
        hline(mx - 10, my, 20, (10, 10, 10), 2)
        vline(mx, my - 10, 20, (10, 10, 10), 2)
    outline(x0, y0, w, h, NAVY, 2)


def draw_hero():
    draw_text(20, 100, "HORMUZ  \u2022  MIDDLE EAST  \u2022  25 NOV 2026", 2, RED)
    draw_text(20, 126, "TANKERS ABLAZE IN", 4, INK)
    draw_text(20, 158, "THE STRAIT OF HORMUZ", 4, INK)
    draw_para(20, 196,
              "Iran's Revolutionary Guards say two oil tankers struck naval "
              "mines in the Strait of Hormuz and caught fire. The vessels had "
              "been transiting an unauthorised route, Tehran says. The US and "
              "Iran have been at war for months, and a US naval blockade is "
              "in force.",
              540, 1, INK, 10)
    draw_text(20, 240, "TWO TANKERS ON FIRE  \u2022  MINES IN THE STRAIT  \u2022  "
                       "BLOCKADE IN FORCE", 1, RED)
    draw_text(20, 262, "ALSO TODAY", 2, RED)
    for i, item in enumerate([
            "490,334 Russian war dead, leaked figures show",
            "Wall Street slides: S&P -2.2%, Nasdaq -3.2%",
            "China flies Pakistan's first astronaut into orbit",
            "COP31 ends with no fossil-fuel deal"]):
        draw_text(20, 284 + i * 14, "\u2022 " + item, 1, INK)
    draw_scene(580, 96, 424, 264)
    draw_para(580, 366,
              "Two tankers burn after mine strikes in the Strait of Hormuz, "
              "25 Nov 2026. The US and Iran are at war; a US blockade is "
              "in force.",
              424, 1, GRAY, 10)


def draw_timeline():
    draw_text(20, 404, "THE DAY IN ORDER  \u2022  25 NOV 2026 (UTC)", 1, NAVY)
    hline(20, 424, 984, NAVY, 2)
    events = [("HORMUZ", "MINES"), ("RAS TANURA", "ATTACK"),
              ("ODESA", "STRIKE"), ("HUAWEI", "VERDICT"),
              ("WALL ST", "SLIDES"), ("COP31", "ENDS"),
              ("SHENZHOU-24", "LAUNCH")]
    for i, (a, b) in enumerate(events):
        cx = 60 + i * 140
        circle(cx, 424, 5, NAVY)
        draw_centered(cx - 70, cx + 70, 434, a, 1, INK)
        draw_centered(cx - 70, cx + 70, 444, b, 1, GRAY)


def draw_lead_card(x, y, w, h, label, headline, body):
    fill_rect(x, y, w, h, CARD)
    outline(x, y, w, h, NAVY, 1)
    draw_text(x + 14, y + 10, label, 1, RED)
    hy = y + 26
    for ln in wrap(headline, w - 28, 2):
        draw_text(x + 14, hy, ln, 2, INK)
        hy += 14
    draw_para(x + 14, hy + 6, body, w - 28, 1, INK, 10)


def draw_grid_card(x, y, w, h, label, headline, body):
    fill_rect(x, y, w, h, CARD)
    outline(x, y, w, h, NAVY, 1)
    draw_text(x + 12, y + 8, label, 1, RED)
    hy = y + 22
    for ln in wrap(headline, w - 24, 2):
        draw_text(x + 12, hy, ln, 2, INK)
        hy += 14
    draw_para(x + 12, hy + 4, body, w - 24, 1, INK, 10)


def draw_page():
    fill_rect(0, 0, W, H, PAPER)
    draw_masthead()
    draw_hero()
    draw_timeline()

    # Three lead stories.
    draw_lead_card(20, 460, 320, 136, "YEMEN  \u2022  25 NOV 2026",
                   "HOUTHIS STRIKE SAUDI REFINERY, RIYADH",
                   "Ras Tanura refinery attacked, fires reported. A strike "
                   "on the PIF tower in Riyadh's financial district injured "
                   "11 people.")
    draw_lead_card(352, 460, 320, 136, "UKRAINE  \u2022  25 NOV 2026",
                   "DEADLY RUSSIAN STRIKES HIT UKRAINE",
                   "Odesa region: 2 killed, 3 hurt, a child among them. "
                   "Kyiv hit, a flat block on fire, 2 hurt. A glide-bomb on "
                   "Zaporizhzhia killed 2 and wounded about 40.")
    draw_lead_card(684, 460, 320, 136, "TECH  \u2022  25 NOV 2026",
                   "HUAWEI GUILTY OF BANK FRAUD IN US",
                   "A US federal jury found Huawei guilty on 10 of 12 "
                   "counts, including bank fraud and conspiracy to steal "
                   "trade secrets. It was acquitted of racketeering.")

    # Eight more stories in a 4x2 grid.
    gx = (20, 269, 518, 767)
    draw_grid_card(gx[0], 604, 237, 128, "GAZA  \u2022  25 NOV 2026",
                   "HAMAS SECURITY CHIEF KILLED",
                   "Israel killed Hamas colonel Mohammad Abuelouf, head of "
                   "interior security, plus his wife and two children.")
    draw_grid_card(gx[1], 604, 237, 128, "RUSSIA  \u2022  25 NOV 2026",
                   "PUTIN VOWS RETALIATION",
                   "Vladimir Putin vowed retaliation over Ukrainian strikes "
                   "on Russian oil refineries, despite Trump's requests to "
                   "refrain.")
    draw_grid_card(gx[2], 604, 237, 128, "RUSSIA  \u2022  25 NOV 2026",
                   "490,334 RUSSIAN WAR DEAD",
                   "Leaked Russian state statistics analysed by the BBC: at "
                   "least 490,334 Russian soldiers have died since the 2022 "
                   "invasion.")
    draw_grid_card(gx[3], 604, 237, 128, "SUDAN  \u2022  25 NOV 2026",
                   "RSF DRONES KILL 19 CIVILIANS",
                   "RSF drone strikes killed 19 civilians and wounded 20 in "
                   "two Sudanese cities, Emergency Lawyers say.")
    draw_grid_card(gx[0], 740, 237, 128, "CLIMATE  \u2022  25 NOV 2026",
                   "COP31 ENDS WITH NO DEAL",
                   "UN climate talks ended with no deal to move away from "
                   "fossil fuels. Pope Leo XIV warned extreme events are "
                   "becoming more frequent.")
    draw_grid_card(gx[1], 740, 237, 128, "PACIFIC  \u2022  25 NOV 2026",
                   "SOLOMONS BAR FOREIGN BASES",
                   "Solomon Islands and Australia signed a treaty "
                   "precluding any foreign military or security base on the "
                   "Solomon Islands.")
    draw_grid_card(gx[2], 740, 237, 128, "TRADE  \u2022  25 NOV 2026",
                   "TRUMP READIES NEW TARIFFS",
                   "Tariffs of 20-40% are being prepared on 14-16 economies "
                   "including China, the EU and Japan. Nothing takes effect "
                   "before a 25 Jan hearing.")
    draw_grid_card(gx[3], 740, 237, 128, "SPACE  \u2022  25 NOV 2026",
                   "PAKISTAN'S FIRST ASTRONAUT FLIES",
                   "China carried Pakistan's first astronaut, Muhammad "
                   "Zeeshan Ali, into orbit on Shenzhou-24 with two Chinese "
                   "crew members.")

    # In brief: the last eight stories.
    draw_text(20, 878, "IN BRIEF  \u2022  25 NOV 2026", 2, NAVY)
    hline(20, 894, 984, NAVY, 1)
    brief_left = [
        "Trump and Zelenskyy meet today; Kyiv seeks EUR 115bn aid for 2027.",
        "Iowa: Army to detonate 5 tons of degraded explosives in a blast.",
        "Microsoft launches 'Code Red' overhaul after a 24-hour outage.",
        "WHO: three bird flu cases and one death in Washington State, US.",
    ]
    brief_right = [
        "Yemen: strike on buses and trucks kills 26, officials say.",
        "Trump to award Rudy Giuliani the Presidential Medal of Freedom.",
        "Nvidia -4.5% as lawmakers question Trump's role in CEO return.",
        "Markets: S&P 500 -2.2%, Nasdaq -3.2%, Nikkei -2.8%, Kospi -6%.",
    ]
    yy = 900
    for item in brief_left:
        draw_text(20, yy, "\u2022 " + item, 1, INK)
        yy += 12
    yy = 900
    for item in brief_right:
        draw_text(522, yy, "\u2022 " + item, 1, INK)
        yy += 12

    # Markets strip and footer.
    fill_rect(20, 958, 984, 34, NAVY)
    draw_centered(20, 1004, 968,
                  "S&P -2.2%  \u2022  NASDAQ -3.2%  \u2022  NIKKEI -2.8%  "
                  "\u2022  OIL -20% IN NOV",
                  2, WHITE)
    draw_centered(0, W, 1002,
                  "THE WORLD IN ONE PAGE  \u2022  WEDNESDAY 25 NOVEMBER 2026"
                  "  \u2022  20 STORIES  \u2022  ALL EVENTS DATED 25 NOV 2026",
                  1, GRAY)


def main():
    draw_page()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    write_png(path)
    print("wrote", path)


if __name__ == "__main__":
    main()
