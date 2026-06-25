#!/usr/bin/env python3
"""
The Growth Table — PDF Presentation Generator
Canva presentation size: 1920 × 1080 (treating px as pt)
Colors match the live landing page CSS.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import os

# ── Page ─────────────────────────────────────────────────────
W, H = 1920, 1080

# ── Colors (from landing page CSS :root) ─────────────────────
NAVY       = HexColor('#03152A')
BLUE       = HexColor('#0567C1')   # CSS --pumpkin / --blue
LBLUE      = HexColor('#75B9F6')   # CSS --blue-light
TEAL       = HexColor('#00E5C3')   # CSS --endeavor (accent only)
WHITE      = HexColor('#FFFFFF')
OFF_WHITE  = HexColor('#F7F7F7')
GRAY_DARK  = HexColor('#4D4D4D')
GRAY_MID   = HexColor('#C4C4C4')
GRAY_LIGHT = HexColor('#E5E5E5')

# ── Paths ─────────────────────────────────────────────────────
HERE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')


def ap(fname):
    return os.path.join(ASSETS, fname)


# ── Drawing helpers (all y coords are "from top") ─────────────

def _rl(top, h=0):
    """Convert top-origin y to reportlab bottom-origin y."""
    return H - top - h


def box(c, x, top, w, h, color):
    c.setFillColor(color)
    c.rect(x, _rl(top, h), w, h, fill=1, stroke=0)


def hline(c, x1, x2, top, color, lw=1):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x1, _rl(top), x2, _rl(top))


def txt(c, s, x, top, font, size, color, align='left'):
    """Draw text. top = baseline y from top of page."""
    c.setFillColor(color)
    c.setFont(font, size)
    y = _rl(top)
    if align == 'center':
        c.drawCentredString(x, y, s)
    elif align == 'right':
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)


def img(c, fname, x, top, height):
    """Draw logo image scaled to given height. Returns drawn_width."""
    path = ap(fname)
    try:
        ir = ImageReader(path)
        iw, ih = ir.getSize()
        scale  = height / ih
        dw     = iw * scale
        c.drawImage(path, x, _rl(top, height), dw, height, mask='auto')
        return dw
    except Exception as e:
        print(f'  [logo] could not load {fname}: {e}')
        return 0


def logo_lockup(c, x, top, h=60, dark=True):
    """
    Three-logo lockup: ATV | Endeavor | BofA
    dark=True  -> white ATV logo (on navy/blue background)
    dark=False -> black ATV logo (on light background)
    Returns total width drawn.
    """
    atv_file  = 'atv-logo-white.png'  if dark else 'atv-logo-horizontal.png'
    div_color = HexColor('#FFFFFF22')  if dark else GRAY_LIGHT

    cur = x

    # ATV (full height)
    atv_w = img(c, atv_file, cur, top, h)
    cur += atv_w + 28

    # Divider
    box(c, cur, top, 1, h, div_color)
    cur += 1 + 28

    # Endeavor (~75% height, vertically centred)
    end_h = h * 0.82
    end_w = img(c, 'endeavor-logo.png', cur, top + (h - end_h) / 2, end_h)
    cur += end_w + 28

    # Divider
    box(c, cur, top, 1, h, div_color)
    cur += 1 + 28

    # BofA (~85% height, vertically centred)
    bofa_h = h * 0.85
    bofa_w = img(c, 'bofa-logo.png', cur, top + (h - bofa_h) / 2, bofa_h)
    cur += bofa_w

    return cur - x


def pill_label(c, s, x, top, bg=None, fg=WHITE):
    """Draw uppercase pill tag. Returns (width, height)."""
    if bg is None:
        bg = BLUE
    font, size = 'Helvetica-Bold', 20
    c.setFont(font, size)
    tw = c.stringWidth(s, font, size)
    pw, ph = tw + 32, 36
    box(c, x, top, pw, ph, bg)
    txt(c, s, x + 16, top + ph - 10, font, size, fg)
    return pw, ph


def rule(c, x, top, w, color=BLUE, h=3):
    box(c, x, top, w, h, color)


# ─────────────────────────────────────────────────────────────
# SLIDE 1  ·  COVER
# ─────────────────────────────────────────────────────────────
def slide_cover(c):
    # Full navy background
    box(c, 0, 0, W, H, NAVY)

    # Right-side darker strip for depth
    box(c, W - 520, 0, 520, H, HexColor('#020e1d'))

    # Blue vertical bar separating the strips
    box(c, W - 528, 0, 6, H, BLUE)

    # Teal top accent mark
    box(c, 80, 72, 90, 4, TEAL)

    # Eyebrow
    txt(c, 'ENDEAVOR SOUTHEAST  x  ATLANTA TECH VILLAGE',
        80, 98, 'Helvetica', 22, TEAL)

    # Giant stacked title
    txt(c, 'THE',    80, 232, 'Helvetica-Bold', 158, WHITE)
    txt(c, 'GROWTH', 80, 415, 'Helvetica-Bold', 158, BLUE)
    txt(c, 'TABLE',  80, 598, 'Helvetica-Bold', 158, WHITE)

    # Subtitle
    txt(c, 'A GROWTH-STAGE FOUNDER PROGRAM',
        80, 670, 'Helvetica', 28, GRAY_MID)

    # Rule
    rule(c, 80, 690, 240, BLUE)

    # Tagline
    txt(c, 'Real partnerships. Real revenue. Real scale.',
        80, 726, 'Helvetica-Oblique', 30, HexColor('#FFFFFF77'))

    # Powered by
    txt(c, 'POWERED BY BANK OF AMERICA',
        80, 770, 'Helvetica', 20, HexColor('#FFFFFF44'))

    # Logo lockup — bottom-left
    logo_lockup(c, 80, H - 148, h=72, dark=True)


# ─────────────────────────────────────────────────────────────
# SLIDE 2  ·  ABOUT
# ─────────────────────────────────────────────────────────────
def slide_about(c):
    box(c, 0, 0, W, H, WHITE)

    # Navy header band
    box(c, 0, 0, W, 148, NAVY)
    txt(c, 'THE GROWTH TABLE',
        80, 60, 'Helvetica-Bold', 56, WHITE)
    txt(c, 'A GROWTH-STAGE FOUNDER PROGRAM',
        80, 122, 'Helvetica', 24, LBLUE)

    # LEFT COLUMN
    lx = 80
    pill_label(c, 'ABOUT THE PROGRAM', lx, 182, BLUE)

    txt(c, 'The premier program connecting',
        lx, 262, 'Helvetica-Bold', 44, NAVY)
    txt(c, 'corporates with growth-stage founders.',
        lx, 318, 'Helvetica-Bold', 44, NAVY)

    rule(c, lx, 346, 80, BLUE)

    body = [
        'A monthly breakfast for growth-stage founders across the Southeast',
        'to learn from top operators and build the corporate relationships',
        'that drive real revenue.',
        '',
        'A joint initiative of Endeavor Southeast and Atlanta Tech Village,',
        'powered by Bank of America.',
    ]
    by = 382
    for line in body:
        if line:
            txt(c, line, lx, by, 'Helvetica', 27, GRAY_DARK)
        by += 44

    # RIGHT PANEL
    rx = 1060
    box(c, rx, 160, W - rx - 60, H - 220, OFF_WHITE)
    box(c, rx, 160, 5, H - 220, BLUE)

    txt(c, 'WHAT MAKES THIS DIFFERENT',
        rx + 32, 210, 'Helvetica-Bold', 26, BLUE)
    rule(c, rx + 32, 242, 130, BLUE, 2)

    points = [
        ('OPERATOR-FIRST',  'Designed for founders scaling, not raising'),
        ('CURATED ACCESS',  'Selective -- not a mass-market event'),
        ('CORPORATE DEALS', 'Direct access to enterprise decision-makers'),
        ('SOUTHEAST FOCUS', 'The region is the point, not a footnote'),
        ('CLOSED DOOR',     'High-trust, candid founder conversations'),
        ('REAL OUTCOMES',   'Revenue, relationships, and real-world scale'),
    ]
    hy = 278
    for title, desc in points:
        box(c, rx + 32, hy, 5, 50, BLUE)
        txt(c, title, rx + 52, hy + 18, 'Helvetica-Bold', 22, NAVY)
        txt(c, desc,  rx + 52, hy + 44, 'Helvetica', 20, GRAY_DARK)
        hy += 82

    # Footer nav
    box(c, 0, H - 52, W, 52, NAVY)
    logo_lockup(c, 80, H - 46, h=30, dark=True)


# ─────────────────────────────────────────────────────────────
# SLIDE 3  ·  PROGRAM PILLARS
# ─────────────────────────────────────────────────────────────
def slide_pillars(c):
    box(c, 0, 0, W, H, NAVY)

    # Header band
    box(c, 0, 0, W, 174, HexColor('#020e1d'))
    txt(c, 'PROGRAM PILLARS', 80, 64, 'Helvetica-Bold', 56, WHITE)
    txt(c, 'Five tracks. One focus: scale.', 80, 134, 'Helvetica', 28, LBLUE)

    # Logo lockup right-aligned in header
    logo_lockup(c, W - 680, 54, h=52, dark=True)

    pillars = [
        ('01', 'Corporate Access\n& Commercial\nPartnerships', [
            'Selling into enterprise',
            'Pilots to contracts',
            'Procurement navigation',
            'Corporate reverse pitches',
        ]),
        ('02', 'Scaling\nOperations', [
            'Hiring executive teams',
            'Org design at scale',
            'Margin and efficiency',
            'Internal systems',
        ]),
        ('03', 'Founder to\nFounder Exchange', [
            'Closed door, high trust',
            'Real time problem solving',
            "What's breaking right now",
        ]),
        ('04', 'Market Expansion\n& Distribution', [
            'Entering new markets',
            'Enterprise distribution',
            'Strategic partnerships',
        ]),
        ('05', 'Beyond VC:\nUncommon Operators', [
            'Global founders',
            'Endeavor mentors & board',
            'Athletes, creators, billionaires',
            'Perspective + execution',
        ]),
    ]

    n        = len(pillars)
    gap      = 5
    margin   = 80
    avail    = W - 2 * margin
    col_w    = (avail - gap * (n - 1)) // n
    card_top = 192
    card_h   = H - card_top - 16

    for i, (num, title, items) in enumerate(pillars):
        cx = margin + i * (col_w + gap)

        box(c, cx, card_top, col_w, card_h, HexColor('#02111f'))
        box(c, cx, card_top, col_w, 4, BLUE)

        # Number
        txt(c, num, cx + 24, card_top + 48, 'Courier', 28, BLUE)
        txt(c, '/ 05', cx + 24 + 58, card_top + 48, 'Courier', 19, HexColor('#FFFFFF44'))

        # Title
        title_lines = title.split('\n')
        ty = card_top + 100
        for tl in title_lines:
            txt(c, tl.upper(), cx + 24, ty, 'Helvetica-Bold', 22, WHITE)
            ty += 30

        # Separator
        rule(c, cx + 24, ty + 10, col_w - 48, HexColor('#FFFFFF22'), 1)

        # Items
        iy = ty + 34
        for item in items:
            txt(c, item, cx + 24, iy, 'Helvetica', 20, HexColor('#FFFFFFBB'))
            iy += 38


# ─────────────────────────────────────────────────────────────
# SLIDE 4  ·  EVENT FORMAT
# ─────────────────────────────────────────────────────────────
def slide_format(c):
    box(c, 0, 0, W, H, WHITE)

    # Left navy panel
    box(c, 0, 0, 420, H, NAVY)

    # Left panel text
    txt(c, 'EVENT',  50, 188, 'Helvetica-Bold', 110, WHITE)
    txt(c, 'FORMAT', 50, 318, 'Helvetica-Bold', 110, BLUE)

    rule(c, 50, 314, 200, TEAL, 3)


    # Large "90" stat
    txt(c, '90',       50, 540, 'Helvetica-Bold', 128, BLUE)
    txt(c, 'MINUTES',  50, 644, 'Helvetica-Bold', 28,  LBLUE)
    txt(c, 'TOTAL PROGRAM TIME', 50, 678, 'Helvetica', 19, HexColor('#FFFFFF55'))

    # Logos bottom of left panel
    logo_lockup(c, 42, H - 106, h=44, dark=True)

    # Right: 3 format blocks stacked
    blocks = [
        ('9:00', 'AM', 'FEATURED CONVERSATION',
         'One featured corporate leader or global operator',
         'in conversation with a moderator.'),
        ('9:30', 'AM', 'MODERATED DISCUSSION',
         'Table-level conversation -- founders engage directly,',
         'ask real questions, share real problems.'),
        ('10:00', 'AM', 'CURATED NETWORKING',
         'Facilitated introductions between founders and',
         'corporate leaders. No cold approaches.'),
    ]

    bx    = 460
    bw    = W - bx - 64
    gap   = 8
    total = H - 64
    bh    = (total - gap * 2) // 3

    for i, (time_val, ampm, label, d1, d2) in enumerate(blocks):
        by = 32 + i * (bh + gap)

        box(c, bx, by, bw, bh, OFF_WHITE)

        # Time badge (navy box left side)
        box(c, bx, by, 188, bh, NAVY)
        cx_badge = bx + 94
        txt(c, time_val, cx_badge, by + bh // 2 - 24,
            'Helvetica-Bold', 64, BLUE, align='center')
        txt(c, ampm, cx_badge, by + bh // 2 + 48,
            'Helvetica-Bold', 22, LBLUE, align='center')

        # Label
        txt(c, label, bx + 208, by + 58, 'Helvetica-Bold', 28, BLUE)

        # Description lines
        txt(c, d1, bx + 208, by + 104, 'Helvetica', 25, GRAY_DARK)
        txt(c, d2, bx + 208, by + 136, 'Helvetica', 25, GRAY_DARK)


# ─────────────────────────────────────────────────────────────
# SLIDE 5  ·  2026 CALENDAR
# ─────────────────────────────────────────────────────────────
def slide_calendar(c):
    box(c, 0, 0, W, H, OFF_WHITE)

    # Header band
    box(c, 0, 0, W, 110, NAVY)
    txt(c, 'Seven sessions. Seven opportunities.', 80, 76, 'Helvetica-Bold', 54, WHITE)

    sessions = [
        ('JULY 28, 2026',   'Selling into\nEnterprise',        True),
        ('AUG 25, 2026',    'Retail\nDistribution',            False),
        ('SEPT 29, 2026',   'Healthcare:\nPilots to Contracts', False),
        ('OCT 27, 2026',    'AI for\nOperators',               False),
        ('NOV 17, 2026',    'Partnerships\nat Scale',          False),
        ('DEC 15, 2026',    'Hiring Your\nExec Team',          False),
        ('JAN 26, 2027',    'TBD',                             False),
    ]

    cols = 4
    rows = 2
    pad  = 8
    gx   = 80
    gy   = 128
    gw   = W - 160
    gh   = H - gy - 18
    cw   = (gw - pad * (cols - 1)) // cols
    ch   = (gh - pad * (rows - 1)) // rows

    for i, (date, theme, featured) in enumerate(sessions):
        row = i // cols
        col = i % cols
        cx  = gx + col * (cw + pad)
        cy  = gy + row * (ch + pad)

        if featured:
            card_bg     = NAVY
            theme_color = WHITE
            date_color  = BLUE
            bar_color   = LBLUE
            tag_bg      = LBLUE
            tag_fg      = NAVY
            tag_text    = 'NOW OPEN'
        else:
            card_bg     = WHITE
            theme_color = NAVY
            date_color  = BLUE
            bar_color   = BLUE
            tag_bg      = GRAY_LIGHT
            tag_fg      = GRAY_DARK
            tag_text    = 'COMING SOON'

        box(c, cx, cy, cw, ch, card_bg)
        box(c, cx, cy, cw, 4, bar_color)

        # Date
        txt(c, date, cx + 28, cy + 50, 'Courier', 22, date_color)

        # Theme (1-2 lines)
        tlines = theme.split('\n')
        ty = cy + 104
        for tl in tlines:
            txt(c, tl.upper(), cx + 28, ty, 'Helvetica-Bold', 30, theme_color)
            ty += 40

        # Tag pill
        tw_tag = 160 if featured else 190
        box(c, cx + 28, cy + ch - 38, tw_tag, 27, tag_bg)
        txt(c, tag_text, cx + 28 + tw_tag // 2, cy + ch - 18,
            'Helvetica-Bold', 16, tag_fg, align='center')


# ─────────────────────────────────────────────────────────────
# SLIDE 6  ·  CTA
# ─────────────────────────────────────────────────────────────
def slide_cta(c):
    box(c, 0, 0, W, H, BLUE)

    # Dark left accent bar
    box(c, 0, 0, 10, H, NAVY)

    # Decorative concentric arcs (bottom-right corner)
    c.setStrokeColor(HexColor('#FFFFFF10'))
    c.setLineWidth(2)
    for r in (680, 520, 380, 250):
        c.circle(W + 60, H + 60, r, fill=0, stroke=1)

    # Eyebrow
    txt(c, 'JOIN THE TABLE', 80, 152, 'Helvetica-Bold', 28, LBLUE)
    rule(c, 80, 180, 80, HexColor('#FFFFFF55'), 3)

    # Headline
    txt(c, 'THE GROWTH TABLE', 80, 310, 'Helvetica-Bold', 112, WHITE)
    txt(c, 'IS NOW ACCEPTING', 80, 440, 'Helvetica-Bold', 68, HexColor('#FFFFFFCC'))
    txt(c, 'GROWTH-STAGE FOUNDERS', 80, 524, 'Helvetica-Bold', 68, HexColor('#FFFFFFCC'))

    # Details
    txt(c, '$5M-$50M+ revenue  /  Southeast-based or expanding  /  Monthly breakfast series',
        80, 588, 'Helvetica', 28, HexColor('#FFFFFF99'))

    # CTA button
    bx, by, bw, bh = 80, 626, 510, 80
    box(c, bx, by, bw, bh, NAVY)
    txt(c, 'REGISTER FOR JULY 28', bx + bw // 2, by + 52,
        'Helvetica-Bold', 28, WHITE, align='center')

    # Tagline
    txt(c, 'Real partnerships. Real revenue. Real scale.',
        80, 758, 'Helvetica-Oblique', 36, HexColor('#FFFFFF88'))

    # Partner credit
    txt(c, 'ENDEAVOR SOUTHEAST x ATLANTA TECH VILLAGE  |  POWERED BY BANK OF AMERICA',
        80, 806, 'Helvetica', 20, HexColor('#FFFFFF66'))

    # Logo lockup
    logo_lockup(c, 80, H - 148, h=72, dark=True)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    output = os.path.join(HERE, 'Growth_Table_Presentation.pdf')

    c = canvas.Canvas(output, pagesize=(W, H))
    c.setTitle('The Growth Table — Presentation')
    c.setAuthor('Atlanta Tech Village')
    c.setSubject('A Growth-Stage Founder Program | Powered by Bank of America')

    slides = [
        ('Cover',    slide_cover),
        ('About',    slide_about),
        ('Pillars',  slide_pillars),
        ('Format',   slide_format),
        ('Calendar', slide_calendar),
        ('CTA',      slide_cta),
    ]

    for i, (name, fn) in enumerate(slides, 1):
        print(f'  Slide {i}/{len(slides)}: {name}')
        fn(c)
        c.showPage()

    c.save()
    print(f'\n  Saved: {output}')


if __name__ == '__main__':
    main()
