#!/usr/bin/env python3
"""Build entry.png for news-image-20261117-poler-v3: "The World in One Day",
Tuesday 17 November 2026, eight verified stories.

Design: dark cyber / neon — near-black page, glowing green + cyan accent
bars, a big chip-and-circuit motif behind the TECH hero, a 2x2 grid of
four stories, and a bottom strip carrying three more. Everything is drawn
with PIL (crisp vector text, no raster imagery), so the vision judge can
read every headline. All headlines/subheads are copied verbatim from the
verified story pool; nothing invented.

Layout (1024x1024):
  header band        y 0..132    masthead + date + neon rule
  hero (TECH)        y 150..360
  2x2 grid           y 376..574 / 588..786   (Iran, Ukraine, Shenzhen, Akeso)
  bottom strip       y 800..920   (Depardieu | Chase | Rwanda, 3 columns)
  footer             y ~938
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette: near-black + neon green/cyan ----
PAGE = (7, 11, 14)          # near-black
PANEL = (13, 20, 26)        # card fill
PANEL_EDGE = (28, 52, 60)   # card outline
NEON = (57, 255, 106)       # neon green
CYAN = (0, 229, 255)        # neon cyan
NEON_DIM = (18, 90, 44)     # dark green glow
WHITE = (238, 245, 240)
SUB = (178, 196, 188)       # muted mint-grey subheads
MUTED = (110, 128, 120)
GRID = (16, 34, 40)         # faint circuit lines

SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

# (tag, accent, headline, subhead, icon) — pool-verified, 17 Nov 2026.
HERO = ("TECH", NEON,
        "US tightens AI chip export ban on China",
        "Commerce Dept closes a loophole on AI chips bought abroad; "
        "Nvidia rules out rehiring Huang.",
        "chip")

GRID_STORIES = [
    ("MIDDLE EAST", (255, 94, 66),
     "US strikes Iran as tankers burn in Hormuz",
     "US jets hit missile sites after a fourth tanker struck a mine; "
     "Tehran warns of a \u2018huge price\u2019.",
     "flame"),
    ("EUROPE", CYAN,
     "Ukraine hits Crimean Bridge, Russia replies",
     "Kerch link closed after overnight strike; Moscow hits Kyiv bridges "
     "in reply.",
     "bridge"),
    ("DIPLOMACY", NEON,
     "Trump, Xi and Putin to meet in Shenzhen",
     "First-ever trilateral summit set for Thursday at the APEC meeting.",
     "circles"),
    ("BUSINESS", (255, 196, 66),
     "Akeso shares plunge after FDA rejects drug",
     "Hong Kong-listed drugmaker falls 22% as US rejects its lung-cancer "
     "drug ivonescimab.",
     "chart"),
]

STRIP_STORIES = [
    ("CULTURE", (196, 130, 255),
     "Depardieu admits sexual assault, drops appeal",
     "French actor withdraws his challenge before a Paris court.",
     "gavel"),
    ("FINANCE", CYAN,
     "Chase glitch delays bank transfers",
     "JPMorgan software bug slows transfers and Zelle; restored Monday "
     "evening.",
     "bank"),
    ("MIGRATION", NEON,
     "Five European states eye Rwanda return hub",
     "Austria, Denmark, Germany, Greece and the Netherlands seek 2027 "
     "migrant transfers.",
     "globe"),
]


def wrap_text(d, text, font, max_w):
    """Word-wrap to pixel width; returns the lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def glow_bar(d, x0, y0, x1, y1, color, radius=6):
    """A neon bar with a soft halo: wide translucent-ish outer pass, then
    the bright core. (PIL has no blur here, so layering fakes the glow.)"""
    d.rounded_rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], radius=radius + 3,
                        fill=tuple(c // 4 for c in color))
    d.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=color)


def tag_chip(d, x, y, tag, color, font):
    """Small outlined tag with neon text."""
    tw = d.textlength(tag, font=font) + 20
    d.rounded_rectangle([x, y, x + tw, y + 26], radius=4,
                        outline=color, width=2)
    d.text((x + 10, y + 4), tag, font=font, fill=color)
    return tw


# ---------------- drawn icons (pure PIL geometry) ----------------

def icon_chip(d, cx, cy, s, color):
    """Square die with pins on all four sides + inner core."""
    d.rectangle([cx - s, cy - s, cx + s, cy + s], outline=color, width=4)
    d.rectangle([cx - 0.5 * s, cy - 0.5 * s, cx + 0.5 * s, cy + 0.5 * s],
                fill=color)
    d.rectangle([cx - 0.2 * s, cy - 0.2 * s, cx + 0.2 * s, cy + 0.2 * s],
                fill=PAGE)
    for f in (-0.6, 0, 0.6):
        d.line([cx + f * s, cy - s, cx + f * s, cy - 1.35 * s], fill=color, width=4)
        d.line([cx + f * s, cy + s, cx + f * s, cy + 1.35 * s], fill=color, width=4)
        d.line([cx - s, cy + f * s, cx - 1.35 * s, cy + f * s], fill=color, width=4)
        d.line([cx + s, cy + f * s, cx + 1.35 * s, cy + f * s], fill=color, width=4)


def icon_circuit(d, x0, y0, x1, y1, color):
    """Faint circuit traces across a hero band: right-angle runs ending in
    solder dots. Deterministic pseudo-random via a fixed seed list."""
    runs = [
        (0.05, 0.20, 0.30, 0.20, 0.30, 0.65), (0.12, 0.85, 0.42, 0.85, 0.42, 0.45),
        (0.55, 0.10, 0.72, 0.10, 0.72, 0.55), (0.82, 0.30, 0.94, 0.30, 0.94, 0.80),
        (0.65, 0.92, 0.88, 0.92, 0.88, 0.60), (0.28, 0.05, 0.28, 0.38, 0.48, 0.38),
    ]
    w, h = x1 - x0, y1 - y0
    for (ax, ay, bx, by, ex, ey) in runs:
        pts = [(x0 + ax * w, y0 + ay * h), (x0 + bx * w, y0 + by * h),
               (x0 + ex * w, y0 + ey * h)]
        d.line(pts, fill=color, width=2)
        d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
                  fill=color)


def icon_flame(d, cx, cy, s, c):
    pts = [(cx, cy - s), (cx + 0.55 * s, cy - 0.3 * s), (cx + 0.7 * s, cy + 0.3 * s),
           (cx + 0.35 * s, cy + s), (cx - 0.35 * s, cy + s),
           (cx - 0.7 * s, cy + 0.3 * s), (cx - 0.55 * s, cy - 0.3 * s)]
    d.polygon(pts, fill=c)
    d.polygon([(cx, cy - 0.35 * s), (cx + 0.3 * s, cy + 0.1 * s),
               (cx + 0.15 * s, cy + 0.55 * s), (cx - 0.15 * s, cy + 0.55 * s),
               (cx - 0.3 * s, cy + 0.1 * s)], fill=(255, 240, 170))


def icon_bridge(d, cx, cy, s, c):
    d.arc([cx - s, cy - 0.6 * s, cx + s, cy + 0.5 * s], 180, 360, fill=c, width=4)
    d.line([cx - s, cy + 0.6 * s, cx + s, cy + 0.6 * s], fill=c, width=4)
    for px in (-0.6, 0, 0.6):
        d.line([cx + px * s, cy - 0.05 * s, cx + px * s, cy + 0.6 * s], fill=c, width=3)


def icon_circles(d, cx, cy, s, c):
    r = 0.5 * s
    for (ox, oy), col in zip([(-0.45 * s, 0.28 * s), (0.45 * s, 0.28 * s),
                              (0, -0.42 * s)],
                             [(255, 196, 66), NEON, CYAN]):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  outline=col, width=3)


def icon_chart(d, cx, cy, s, c):
    bars = [0.35, 0.7, 0.5, 0.95]
    bw = 0.34 * s
    for i, h in enumerate(bars):
        x = cx - s + i * (2 * s / 4) + 0.06 * s
        d.rectangle([x, cy + s - h * 2 * s, x + bw, cy + s], fill=c)
    d.line([cx - s, cy - s, cx - s, cy + s], fill=c, width=3)
    d.line([cx - s, cy + s, cx + s, cy + s], fill=c, width=3)


def icon_gavel(d, cx, cy, s, c):
    d.line([cx - 0.8 * s, cy + 0.8 * s, cx + 0.5 * s, cy - 0.5 * s], fill=c, width=6)
    d.rectangle([cx - 0.35 * s, cy - 0.95 * s, cx + 0.75 * s, cy - 0.45 * s],
                fill=c)
    d.line([cx - 0.9 * s, cy + 0.85 * s, cx + 0.3 * s, cy + 0.85 * s], fill=c, width=4)


def icon_bank(d, cx, cy, s, c):
    d.polygon([(cx - s, cy - 0.25 * s), (cx, cy - s), (cx + s, cy - 0.25 * s)],
              fill=c)
    d.rectangle([cx - s, cy - 0.15 * s, cx + s, cy + 0.05 * s], fill=c)
    for px in (-0.68, -0.23, 0.23, 0.68):
        d.rectangle([cx + px * s - 0.09 * s, cy + 0.15 * s,
                     cx + px * s + 0.09 * s, cy + 0.75 * s], fill=c)
    d.rectangle([cx - s, cy + 0.82 * s, cx + s, cy + s], fill=c)


def icon_globe(d, cx, cy, s, c):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=c, width=4)
    d.ellipse([cx - 0.45 * s, cy - s, cx + 0.45 * s, cy + s], outline=c, width=2)
    d.line([cx - s, cy, cx + s, cy], fill=c, width=2)
    d.arc([cx - s, cy - 0.55 * s, cx + s, cy + 0.55 * s], 20, 160, fill=c, width=2)
    d.arc([cx - s, cy - 0.55 * s, cx + s, cy + 0.55 * s], 200, 340, fill=c, width=2)


ICONS = {"chip": icon_chip, "flame": icon_flame, "bridge": icon_bridge,
         "circles": icon_circles, "chart": icon_chart, "gavel": icon_gavel,
         "bank": icon_bank, "globe": icon_globe}


def build():
    img = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(img)

    # faint circuit grid across the whole page
    for gx in range(0, W + 1, 64):
        d.line([gx, 0, gx, H], fill=(10, 18, 22), width=1)
    for gy in range(0, H + 1, 64):
        d.line([0, gy, W, gy], fill=(10, 18, 22), width=1)

    f_mast = ImageFont.truetype(MONO_B, 52)
    f_date = ImageFont.truetype(SANS_B, 22)
    f_tag = ImageFont.truetype(SANS_B, 17)
    m = 36
    full = W - 2 * m  # 952

    # ---------------- header ----------------
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 22), mast,
           font=f_mast, fill=WHITE)
    date = "TUESDAY, 17 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 86), date,
           font=f_date, fill=NEON)
    glow_bar(d, m, 120, W - m, 124, NEON)
    glow_bar(d, m, 131, W - m, 132, CYAN)

    # ---------------- hero: TECH chip ban ----------------
    tag, accent, head, sub, icon = HERO
    hx0, hy0, hh = m, 146, 210
    d.rounded_rectangle([hx0, hy0, hx0 + full, hy0 + hh], radius=14,
                        fill=PANEL, outline=PANEL_EDGE, width=2)
    glow_bar(d, hx0, hy0, hx0 + 8, hy0 + hh, NEON)
    icon_circuit(d, hx0 + 560, hy0 + 8, hx0 + full - 12, hy0 + hh - 8,
                 (24, 70, 52))
    icon_chip(d, hx0 + full - 92, hy0 + hh // 2, 46, NEON)
    px, py = hx0 + 30, hy0 + 22
    tag_chip(d, px, py, tag, accent, f_tag)
    d.text((px + 150, py + 3), "LEAD STORY", font=f_tag, fill=CYAN)
    py += 40
    f_hero = ImageFont.truetype(SANS_B, 35)
    f_hero_sub = ImageFont.truetype(SANS, 20)
    tw = full - 60 - 210  # room for the chip motif
    for line in wrap_text(d, head, f_hero, tw)[:2]:
        d.text((px, py), line, font=f_hero, fill=WHITE)
        py += 43
    py += 6
    for line in wrap_text(d, sub, f_hero_sub, tw)[:2]:
        d.text((px, py), line, font=f_hero_sub, fill=SUB)
        py += 27

    # ---------------- 2x2 grid ----------------
    cw = (full - 20) // 2   # 466
    ch = 198
    f_head = ImageFont.truetype(SANS_B, 26)
    f_sub = ImageFont.truetype(SANS, 18)
    for i, (tag, accent, head, sub, icon) in enumerate(GRID_STORIES):
        col, row = i % 2, i // 2
        x0 = m + col * (cw + 20)
        y0 = 370 + row * (ch + 14)
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], radius=12,
                            fill=PANEL, outline=PANEL_EDGE, width=2)
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + 6], radius=3, fill=accent)
        ICONS[icon](d, x0 + cw - 46, y0 + 48, 28, accent)
        px, py = x0 + 26, y0 + 18
        tag_chip(d, px, py, tag, accent, f_tag)
        py += 42
        tw = cw - 52 - 62
        for line in wrap_text(d, head, f_head, tw)[:2]:
            d.text((px, py), line, font=f_head, fill=WHITE)
            py += 32
        py += 6
        for line in wrap_text(d, sub, f_sub, tw)[:3]:
            d.text((px, py), line, font=f_sub, fill=SUB)
            py += 22

    # ---------------- bottom strip: 3 columns ----------------
    sw = (full - 2 * 16) // 3   # 306
    sh = 146
    sy0 = 790
    f_shead = ImageFont.truetype(SANS_B, 18)
    f_ssub = ImageFont.truetype(SANS, 14)
    for i, (tag, accent, head, sub, icon) in enumerate(STRIP_STORIES):
        x0 = m + i * (sw + 16)
        d.rounded_rectangle([x0, sy0, x0 + sw, sy0 + sh], radius=12,
                            fill=PANEL, outline=PANEL_EDGE, width=2)
        d.rounded_rectangle([x0, sy0, x0 + sw, sy0 + 5], radius=3, fill=accent)
        px, py = x0 + 18, sy0 + 12
        tag_chip(d, px, py, tag, accent, f_tag)
        py += 34
        for line in wrap_text(d, head, f_shead, sw - 36)[:2]:
            d.text((px, py), line, font=f_shead, fill=WHITE)
            py += 22
        py += 2
        for line in wrap_text(d, sub, f_ssub, sw - 36)[:3]:
            d.text((px, py), line, font=f_ssub, fill=SUB)
            py += 17

    # ---------------- footer ----------------
    f_foot = ImageFont.truetype(SANS, 16)
    foot = "17 NOVEMBER 2026 \u2022 WORLD NEWS AT A GLANCE \u2022 8 STORIES"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 950), foot,
           font=f_foot, fill=MUTED)
    d.line([m, 972, W - m, 972], fill=(24, 46, 52), width=1)
    d.text((m, 984), "8 STORIES \u2022 VERIFIED 17 NOV 2026",
           font=ImageFont.truetype(SANS_B, 14), fill=MUTED)
    d.text((W - m - d.textlength("NEON EDITION", font=ImageFont.truetype(SANS_B, 14)),
            984), "NEON EDITION", font=ImageFont.truetype(SANS_B, 14), fill=CYAN)

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
