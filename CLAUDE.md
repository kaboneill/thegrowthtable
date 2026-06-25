# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**The Growth Table** is a branded event program — a monthly breakfast series for growth-stage founders ($5M–$50M+ revenue), jointly run by Endeavor Southeast and Atlanta Tech Village, powered by Bank of America. This repo generates the program's marketing assets: a PDF slide deck, a social media graphic, and a landing page.

## Generating Assets

```bash
# PDF presentation (6 slides, output: Growth_Table_Presentation.pdf)
python3 generate_slides.py

# Social share graphic (output: Growth_Table_Social.png)
python3 generate_graphic.py
```

Dependencies: `reportlab` (PDF), `Pillow` (social image). Install with `pip3 install reportlab Pillow`.

The landing page (`index.html`) is static — open it directly in a browser or deploy via Netlify (`.netlify/` config is present).

## Architecture

Three independent output generators share the same design system:

| File | Output | Renderer |
|------|--------|----------|
| `generate_slides.py` | `Growth_Table_Presentation.pdf` | reportlab |
| `generate_graphic.py` | `Growth_Table_Social.png` | Pillow |
| `index.html` | Landing page | Static HTML/CSS |

All three reference logos from `assets/` (four PNGs: ATV horizontal, ATV white, Endeavor, BofA). Colors are defined independently in each file but must stay in sync — see `branding.md` for the canonical palette.

**Coordinate system in generate_slides.py**: reportlab uses bottom-left origin; the helpers `_rl(top, h)` convert from top-origin (where `top` = distance from the top of the page). All positioning in the slide functions uses top-origin values.

## Branding Rules (enforced in code)

- **Logo lockup order**: ATV left → Endeavor center → BofA right, separated by 1px dividers
- **Dark backgrounds**: use `atv-logo-white.png`; light backgrounds: use `atv-logo-horizontal.png`
- **Primary palette**: Navy `#03152A`, Blue `#0567C1`, Light Blue `#75B9F6`, Teal `#00E5C3` (Endeavor accent only), White `#FFFFFF`
- **Teal and BofA colors** are logo/accent-only — never use as fills or button backgrounds
- Full brand rules in `branding.md`

## 2026 Session Calendar

| Date | Theme |
|------|-------|
| July 28, 2026 | Selling into Enterprise |
| August 25, 2026 | Retail Distribution |
| September 29, 2026 | Healthcare: Pilots → Contracts |
| October 27, 2026 | AI for Operators |
| November 17, 2026 | Partnerships at Scale |
| December 15, 2026 | Hiring Your Exec Team |
| January 26, 2027 | TBD |

When updating calendar content, change it in all three outputs: `generate_slides.py` (`slide_calendar`), `index.html` (calendar section), and any social graphics as needed.
