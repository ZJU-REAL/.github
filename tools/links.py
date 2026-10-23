"""Footer link pills (outlined, rounded) for the org profile, one light and one dark SVG per link.

Run from the repository root:  python3 tools/links.py
Writes profile/assets/links/<key>-light.svg and <key>-dark.svg and prints the README footer row.
Brand icons in tools/icons/ come from simple-icons 13.21.0 (CC0).
"""
import os, re
from xml.sax.saxutils import escape
from PIL import ImageFont

OUT = 'profile/assets/links'
FAMILY = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MEASURE = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 14, index=1)   # bold Helvetica, for width estimates
SLACK = 1.08                                                                        # room for wider system fonts

LINE = {  # stroke icons on a 24x24 grid
    'home': 'M3 11 12 4l9 7M5 10v10h5v-6h4v6h5V10',
    'join': 'M15 20v-1a5 5 0 0 0-10 0v1M10 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M19 8v6M16 11h6',
    'pi': 'M4 5h16v14H4zM8 10h.01M7 15c.6-1.5 1.7-2 3-2s2.4.5 3 2M14 9h3M14 12h3',
}
HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = {n: re.search(r' d="([^"]+)"', open(os.path.join(HERE, 'icons', f'{n}.svg')).read()).group(1)
         for n in ('googlescholar', 'xiaohongshu', 'x')}

LINKS = [  # key, label, url, icon, accent
    ('website', 'Lab Website', 'https://zjureal.com', 'home', False),
    ('scholar', 'Google Scholar', 'https://scholar.google.com/citations?user=UT3NzFAAAAAJ', 'googlescholar', False),
    ('rednote', 'RedNote', 'https://www.xiaohongshu.com/user/profile/67d84bef000000000d008f18', 'xiaohongshu', False),
    ('x', '@zjureal', 'https://x.com/zjureal', 'x', False),
    ('pi', 'PI Homepage', 'https://person.zju.edu.cn/shenyongliang', 'pi', False),
    ('join', 'Join Us', 'https://zjureal.com/join.html', 'join', True),
]
INK = {'light': '#004EA2', 'dark': '#8DB4EA'}   # ZJU blue, and its readable tint on GitHub dark
GREEN = '#2E7D5B'                               # Lifelong green for the call to action


def icon(name, colour, x, y, s=16):
    k = s / 24
    if name in LINE:
        return (f'<g transform="translate({x},{y}) scale({k})" fill="none" stroke="{colour}" stroke-width="2.2" '
                f'stroke-linecap="round" stroke-linejoin="round"><path d="{LINE[name]}"/></g>')
    return f'<g transform="translate({x},{y}) scale({k})" fill="{colour}"><path d="{BRAND[name]}"/></g>'


def pill(label, ic, theme, accent):
    w, h = round(14 + 16 + 8 + MEASURE.getlength(label) * SLACK + 16), 34
    fg = '#FFFFFF' if accent else INK[theme]
    fill, fill_op, stroke_op = (GREEN, 1, 1) if accent else (INK[theme], 0.06 if theme == 'light' else 0.10, 0.45)
    stroke = GREEN if accent else INK[theme]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="{(h - 1.5) / 2}" fill="{fill}" fill-opacity="{fill_op}" '
            f'stroke="{stroke}" stroke-opacity="{stroke_op}" stroke-width="1.5"/>'
            + icon(ic, fg, 14, 9)
            + f'<text x="38" y="22" font-family="{FAMILY}" font-size="14" font-weight="600" fill="{fg}">{escape(label)}</text></svg>')


os.makedirs(OUT, exist_ok=True)
row = []
for key, label, url, ic, accent in LINKS:
    for theme in ('light', 'dark'):
        open(os.path.join(OUT, f'{key}-{theme}.svg'), 'w').write(pill(label, ic, theme, accent))
    row.append(f'<a href="{url}"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/links/{key}-dark.svg">'
               f'<img alt="{label}" src="assets/links/{key}-light.svg" height="34"></picture></a>')
print('&nbsp;\n'.join(row))
