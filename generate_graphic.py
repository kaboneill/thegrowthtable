#!/usr/bin/env python3
"""
The Growth Table — Social Share Graphic
Output: Growth_Table_Social.png  (1920 × 1080 px)
"""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1920, 1080

# ── Colors ────────────────────────────────────────────────────
NAVY     = (3,   21,  42)
BLUE     = (5,  103, 193)
LBLUE    = (117, 185, 246)
TEAL     = (0,  229, 195)
WHITE    = (255, 255, 255)
GRAY_MID = (196, 196, 196)

# Pre-blended whites on navy for "dim" text
WHITE_80 = (204, 208, 213)   # white 80% on navy
WHITE_55 = (142, 149, 159)   # white 55% on navy
WHITE_30 = (79,  91, 106)    # white 30% on navy

# ── Paths ─────────────────────────────────────────────────────
HERE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')
FONT   = '/System/Library/Fonts/HelveticaNeue.ttc'


def fnt(size, style='regular'):
    idx = {'regular': 0, 'bold': 1, 'italic': 2}[style]
    return ImageFont.truetype(FONT, size, index=idx)


def paste_logo(img, fname, x, y, height, white=False):
    """Paste logo PNG at (x, y) scaled to height. Returns drawn width."""
    path = os.path.join(ASSETS, fname)
    try:
        logo = Image.open(path).convert('RGBA')
        lw, lh = logo.size
        scale  = height / lh
        new_w  = int(lw * scale)
        logo   = logo.resize((new_w, height), Image.LANCZOS)
        if white:
            r, g, b, a = logo.split()
            white_img = Image.new('RGBA', logo.size, (255, 255, 255, 255))
            white_img.putalpha(a)
            logo = white_img
        img.paste(logo, (int(x), int(y)), logo)
        return new_w
    except Exception as e:
        print(f'  [logo] {fname}: {e}')
        return 0


def logo_lockup(img, draw, x, y, h=60):
    """ATV white | Endeavor | BofA lockup on dark background."""
    cur = x

    atv_w = paste_logo(img, 'atv-logo-white.png', cur, y, h)
    cur  += atv_w + 28

    # Divider
    draw.rectangle([cur, y, cur + 1, y + h], fill=WHITE_30)
    cur += 1 + 28

    end_h = int(h * 0.40)
    end_w = paste_logo(img, 'endeavor-logo.png', cur, y + (h - end_h) // 2, end_h)
    cur  += end_w + 28

    draw.rectangle([cur, y, cur + 1, y + h], fill=WHITE_30)
    cur += 1 + 28

    bofa_h = int(h * 0.85)
    paste_logo(img, 'bofa-logo.png', cur, y + (h - bofa_h) // 2, bofa_h, white=True)


def make_graphic():
    img  = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # ── Decorative concentric arcs (bottom-right corner) ─────
    arc_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    arc_draw    = ImageDraw.Draw(arc_overlay)
    cx, cy = W + 90, H + 90
    for r, alpha in [(740, 14), (580, 18), (430, 22), (300, 26), (185, 30)]:
        arc_draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            outline=(5, 103, 193, alpha), width=2
        )
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, arc_overlay)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)

    # ── Left blue accent bar ──────────────────────────────────
    draw.rectangle([0, 0, 12, H], fill=BLUE)

    # ── Top teal accent line ──────────────────────────────────
    draw.rectangle([0, 0, W, 4], fill=TEAL)

    # ── Eyebrow ───────────────────────────────────────────────
    draw.text((80, 56), 'ENDEAVOR SOUTHEAST  ×  ATLANTA TECH VILLAGE  |  POWERED BY BANK OF AMERICA',
              font=fnt(22), fill=TEAL)

    # ── Main title (stacked) ──────────────────────────────────
    draw.text((80, 130), 'THE',    font=fnt(190, 'bold'), fill=WHITE)
    draw.text((80, 338), 'GROWTH', font=fnt(190, 'bold'), fill=BLUE)
    draw.text((80, 546), 'TABLE',  font=fnt(190, 'bold'), fill=WHITE)

    # ── Subtitle ──────────────────────────────────────────────
    draw.text((80, 752), 'A GROWTH-STAGE FOUNDER PROGRAM',
              font=fnt(28), fill=GRAY_MID)

    # ── Rule ──────────────────────────────────────────────────
    draw.rectangle([80, 778, 330, 781], fill=BLUE)

    # ── Tagline ───────────────────────────────────────────────
    draw.text((80, 798), 'Real partnerships. Real revenue. Real scale.',
              font=fnt(30, 'italic'), fill=WHITE_55)

    # ── Logo lockup ───────────────────────────────────────────
    logo_lockup(img, draw, 80, H - 110, h=62)

    return img


def main():
    img    = make_graphic()
    output = os.path.join(HERE, 'Growth_Table_Social.png')
    img.save(output, 'PNG')
    print(f'  Saved: {output}')
    return output


if __name__ == '__main__':
    main()
