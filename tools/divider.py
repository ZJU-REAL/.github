"""REAL divider: a hairline fading out at both ends, four pillar dots breathing in turn at the centre."""
import os

HERE = 'profile/assets'  # run from the repository root
W, H, CX, CY = 1200, 28, 600, 14
DOTS = {'light': ['#004EA2', '#13808C', '#4A6FA5', '#2E7D5B'],
        'dark': ['#6FA0E0', '#6CC3CC', '#93A9D1', '#7DC4A0']}
LINE = {'light': '#B9C7DD', 'dark': '#3A4A66'}
STYLE = """.d{transform-box:fill-box;transform-origin:center;animation:b 3.2s ease-in-out infinite}
.d1{animation-delay:.4s}.d2{animation-delay:.8s}.d3{animation-delay:1.2s}
@keyframes b{0%,60%,100%{transform:scale(1);opacity:.85}20%{transform:scale(1.6);opacity:1}}
.s{animation:s 6s linear infinite}@keyframes s{from{stroke-dashoffset:0}to{stroke-dashoffset:-48}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}"""


def svg(theme):
    c, ln = DOTS[theme], LINE[theme]
    gap, step = 46, 18
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<style>{STYLE}</style><defs>',
         f'<linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{ln}" stop-opacity="0"/><stop offset="1" stop-color="{ln}"/></linearGradient>',
         f'<linearGradient id="r" x1="0" x2="1"><stop offset="0" stop-color="{ln}"/><stop offset="1" stop-color="{ln}" stop-opacity="0"/></linearGradient>',
         '</defs>',
         f'<rect x="60" y="{CY - 0.75}" width="{CX - gap - 60}" height="1.5" fill="url(#l)"/>',
         f'<rect x="{CX + gap}" y="{CY - 0.75}" width="{W - 60 - CX - gap}" height="1.5" fill="url(#r)"/>',
         # a faint travelling dash on each side, moving toward the centre
         f'<line class="s" x1="{CX - gap - 200}" y1="{CY}" x2="{CX - gap}" y2="{CY}" stroke="{c[0]}" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="10 38" style="animation-direction:reverse"/>',
         f'<line class="s" x1="{CX + gap}" y1="{CY}" x2="{CX + gap + 200}" y2="{CY}" stroke="{c[3]}" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="10 38"/>']
    x0 = CX - 1.5 * step
    for i, col in enumerate(c):
        o.append(f'<circle class="d d{i}" cx="{x0 + i * step:.1f}" cy="{CY}" r="4.2" fill="{col}"/>')
    o.append('</svg>')
    return '\n'.join(o)


for th in DOTS:
    open(os.path.join(HERE, f'divider-{th}.svg'), 'w').write(svg(th))
print('ok')
