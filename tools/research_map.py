"""Animated REAL research map in the website's visual language (CSS + SMIL only, so it plays inside a GitHub README).

Run from the repository root:  python3 tools/research_map.py
Writes profile/assets/research-map-light.svg and research-map-dark.svg.
"""
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
EAGLE = 'M44.1474 66.4569L39.1672 58.8578C40.6965 58.0705 40.5071 55.6155 39.197 55.4113C37.7385 55.1828 36.5775 55.1126 35.5542 52.8197H37.9267L37.1984 50.831C34.4838 51.0694 33.93 50.315 32.6429 48.1947L36.0336 48.0786L35.3481 46.3481C31.6532 46.5195 30.6784 45.6136 29.7558 43.5082L34.061 43.3573L33.129 41.2984C28.7201 41.4214 27.7869 41.2966 26.1701 38.3151L31.647 38.2884L30.8746 36.327C25.8826 36.5424 24.6359 36.0538 23.2227 33.5572L34.4435 33.2734C36.0789 33.2318 37.9459 34.3463 38.6339 35.8296L39.9831 38.741L41.403 33.8409C42.1351 31.3164 47.6523 32.2316 49.428 33.9117L46.0907 35.1187L47.7237 39.0949C48.9071 36.3257 50.3569 33.2722 53.4762 33.2722H64.484C63.6371 35.7042 61.5925 36.9168 57.1482 36.1301L56.3671 38.189L61.8564 38.1723C60.5426 41.2351 59.0847 41.6201 55.0018 41.1556L54.1493 43.2145L58.5191 43.3567C57.6784 45.2976 56.1566 46.458 52.7833 46.0545L52.073 48.0593L55.5525 48.0432C54.5553 50.482 53.9115 51.0265 50.74 50.8837L50.0129 52.8718L52.5194 52.8811C51.4658 55.004 51.1535 55.256 48.9046 55.4554C47.5678 55.5739 46.9718 57.7141 48.7519 58.9826L44.1474 66.4569Z'  # ZJU Qiushi eagle, as on the website

W, H = 1200, 800
CX, CY = 600, 410                 # robot / orbit centre
RX, RY = 390, 262                 # orbit radii
ZONES = {                         # centre of each illustration
    'R': (210, 410), 'E': (600, 148), 'A': (990, 410), 'L': (600, 672),
}
PILLAR = {
    'R': ('Reasoning', 'reasons reliably', '#2563EB', '#7AB0FF'),
    'E': ('Embodied', 'inhabits a body', '#0891B2', '#3FD6EE'),
    'A': ('Agentic', 'acts autonomously', '#7C3AED', '#B79CFF'),
    'L': ('Lifelong', 'learns continuously', '#059669', '#4ADE9E'),
}
FLOW = [  # clockwise hand-offs, label position on the orbit (degrees, SVG angle)
    ('reasoning meets the physical world', 225, 'end'),
    ('physical interaction becomes autonomy', 315, 'start'),
    ('every trajectory becomes experience', 45, 'start'),
    ('experience becomes a better model', 135, 'end'),
]
THEMES = {
    'light': dict(bg='#FFFFFF', ink='#0F172A', soft='#475569', mute='#64748B', card='#FFFFFF', line='#DCE5F3',
                  orbit='#9FB2D0', robot='#3B6FE0', robot_fill='#EEF3FF', halo='#8AA3C2', screen='#F9FAFB', eagle='#004EA2'),
    'dark': dict(bg='#0D1117', ink='#E6EDF3', soft='#B6C2D2', mute='#8B98AB', card='#121A27', line='#24324A',
                 orbit='#4A5C7A', robot='#7AA7FF', robot_fill='#18233A', halo='#3B5B8C', screen='#1B2536', eagle='#7AA7FF'),
}


def col(k, theme):
    return PILLAR[k][2] if theme == 'light' else PILLAR[k][3]


# --------------------------------------------------------------------------- zone scenes (local coords, centred on 0,0)
def scene_reasoning(c):
    # a small thought tree: nodes light up in order, then a check mark confirms the answer
    nodes = [(-94, 8), (-46, -28), (-46, 44), (2, -44), (2, -4), (2, 38), (50, -4)]
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 6)]
    o = []
    for i, (a, b) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        o.append(f'<line class="r-edge" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}"/>')
        o.append(f'<line class="r-sig" style="animation-delay:{-0.35 * i:.2f}s" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(nodes):
        dim = ' r-dead' if i in (3, 5) else ''
        o.append(f'<circle class="r-node{dim}" style="animation-delay:{0.35 * i:.2f}s" cx="{x}" cy="{y}" r="8" fill="{c}"/>')
    # answer -> verified: a short link from the final node to the check ring on its right
    o.append(f'<line class="r-edge" x1="58" y1="-4" x2="75" y2="-4" stroke="{c}"/>')
    o.append(f'<circle class="r-goal" cx="92" cy="-4" r="17" fill="none" stroke="{c}" stroke-width="2"/>')
    o.append(f'<path class="r-check" d="M 83 -4 L 90 4 L 103 -13" fill="none" stroke="{c}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')
    return ''.join(o)


def scene_embodied(c):
    # isometric floor, a floating cube, and a robot arm that reaches for it
    o = [f'<polygon points="0,-30 92,16 0,62 -92,16" fill="{c}" fill-opacity="0.16"/>']
    for k in range(1, 4):
        t = k / 4
        o.append(f'<line x1="{-92 + 92 * t:.1f}" y1="{16 - 46 * t:.1f}" x2="{0 + 92 * t:.1f}" y2="{62 - 46 * t:.1f}" stroke="{c}" stroke-opacity="0.28" stroke-dasharray="2 3"/>')
        o.append(f'<line x1="{-92 + 92 * t:.1f}" y1="{16 + 46 * t:.1f}" x2="{0 + 92 * t:.1f}" y2="{-30 + 46 * t:.1f}" stroke="{c}" stroke-opacity="0.28" stroke-dasharray="2 3"/>')
    o.append('<g class="e-cube">'
             f'<polygon points="30,-36 52,-25 30,-14 8,-25" fill="{c}" fill-opacity="0.9"/>'
             f'<polygon points="8,-25 30,-14 30,10 8,-1" fill="{c}" fill-opacity="0.55"/>'
             f'<polygon points="30,-14 52,-25 52,-1 30,10" fill="{c}" fill-opacity="0.75"/></g>')
    # robot arm on the floor: shoulder and elbow swing so the gripper reaches toward the cube
    o.append('<g transform="translate(-40,30)">'
             f'<ellipse cx="0" cy="2" rx="17" ry="7" fill="{c}" fill-opacity="0.35"/>'
             f'<rect x="-9" y="-12" width="18" height="14" rx="4" fill="{c}" fill-opacity="0.75"/>'
             '<g>'
             '<animateTransform attributeName="transform" type="rotate" values="-24 0 -12;24 0 -12;-24 0 -12" '
             'keyTimes="0;0.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="4s" repeatCount="indefinite"/>'
             f'<line x1="0" y1="-12" x2="0" y2="-46" stroke="{c}" stroke-width="8" stroke-linecap="round"/>'
             f'<circle cx="0" cy="-12" r="6" fill="{c}"/>'
             '<g>'
             '<animateTransform attributeName="transform" type="rotate" values="28 0 -46;80 0 -46;28 0 -46" '
             'keyTimes="0;0.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="4s" repeatCount="indefinite"/>'
             f'<line x1="0" y1="-46" x2="0" y2="-76" stroke="{c}" stroke-width="6.5" stroke-linecap="round"/>'
             f'<circle cx="0" cy="-46" r="5.5" fill="{c}"/>'
             f'<path d="M -7 -74 L -7 -85 M 7 -74 L 7 -85 M -7 -76 L 7 -76" stroke="{c}" stroke-width="3.5" stroke-linecap="round" fill="none"/>'
             '</g></g></g>')
    return ''.join(o)


def scene_agentic(c, t):
    # a code window that types itself and a phone being tapped
    o = [f'<g transform="translate(-112,-52)">'
         f'<rect width="128" height="96" rx="9" fill="{c}" fill-opacity="0.12"/>'
         f'<rect width="128" height="16" rx="9" fill="{c}" fill-opacity="0.28"/><rect y="9" width="128" height="7" fill="{c}" fill-opacity="0.28"/>'
         '<circle cx="11" cy="8" r="2.6" fill="#e06c6c"/><circle cx="20" cy="8" r="2.6" fill="#e0b36c"/><circle cx="29" cy="8" r="2.6" fill="#6cc08a"/>']
    for i, (x, w) in enumerate([(12, 62), (22, 84), (22, 48), (12, 72), (22, 40)]):
        o.append(f'<rect class="a-line" style="animation-delay:{0.45 * i:.2f}s" x="{x}" y="{28 + 12 * i}" width="{w}" height="5" rx="2" fill="{c}" fill-opacity="0.6"/>')
    o.append(f'<rect class="a-cursor" x="66" y="76" width="2.5" height="10" fill="{c}"/></g>')
    o.append(f'<g transform="translate(34,-58)">'
             f'<rect width="64" height="112" rx="13" fill="{c}" fill-opacity="0.85"/>'
             f'<rect x="5" y="10" width="54" height="92" rx="7" fill="{t["screen"]}"/>'
             f'<rect x="22" y="12" width="20" height="4" rx="2" fill="{c}"/>')
    for r in range(3):
        for k in range(3):
            act = ' a-app' if (r, k) == (1, 2) else ''
            o.append(f'<rect class="app{act}" x="{11 + 16 * k}" y="{24 + 16 * r}" width="11" height="11" rx="3" fill="{c}" fill-opacity="{0.85 if act else 0.32}"/>')
    o.append(f'<circle class="a-tap" cx="48.5" cy="45.5" r="9" fill="none" stroke="{c}" stroke-width="1.6"/>')
    o.append(f'<rect x="11" y="78" width="42" height="5" rx="2" fill="{c}" fill-opacity="0.5"/><rect x="11" y="88" width="28" height="5" rx="2" fill="{c}" fill-opacity="0.28"/></g>')
    return ''.join(o)


def scene_lifelong(c):
    # experience bars that keep growing, a loop that keeps turning, a sprout that keeps rising
    o = []
    for i, h in enumerate([26, 40, 56, 74]):
        o.append(f'<rect class="l-bar" style="animation-delay:{0.4 * i:.2f}s" x="{-96 + 26 * i}" y="{30 - h}" width="17" height="{h}" rx="4" fill="{c}" fill-opacity="{0.35 + 0.18 * i:.2f}"/>')
    o.append(f'<line x1="-104" y1="31" x2="6" y2="31" stroke="{c}" stroke-opacity="0.35" stroke-width="1.5"/>')
    o.append(f'<path d="M -96 6 C -70 -2, -44 -18, -10 -50" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="4 4" class="l-trend"/>')
    o.append(f'<g transform="translate(62,-6)"><g class="l-loop">'
             f'<path d="M 26 0 A 26 26 0 1 1 18.4 -18.4" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round"/>'
             f'<path d="M 18.4 -18.4 L 10 -24 M 18.4 -18.4 L 24 -10" stroke="{c}" stroke-width="3" stroke-linecap="round"/></g>'
             f'<g class="l-sprout"><path d="M 0 12 L 0 -4" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/>'
             f'<path d="M 0 -2 C -10 -4, -12 -12, -10 -16 C -4 -14, 0 -10, 0 -2 Z" fill="{c}"/>'
             f'<path d="M 0 -4 C 9 -7, 12 -15, 10 -19 C 3 -17, 0 -12, 0 -4 Z" fill="{c}" fill-opacity="0.75"/></g></g>')
    return ''.join(o)


def robot(t):
    # homepage robot, recentred on (0,0) and topped with the Qiushi eagle
    a = t['robot']
    return (f'<g transform="translate({-220 * 0.9:.1f},{-294 * 0.9:.1f}) scale(0.9)"><g class="bot">'
            f'<g transform="translate(175, 118) scale(1.0225)"><path d="{EAGLE}" fill="{t["eagle"]}" fill-rule="evenodd"/></g>'
            f'<rect x="178" y="208" width="4" height="32" rx="2" transform="rotate(-14 180 224)" fill="{a}"/>'
            f'<rect x="258" y="208" width="4" height="32" rx="2" transform="rotate(14 260 224)" fill="{a}"/>'
            f'<circle class="tip" cx="180" cy="206" r="7" fill="{a}"/><circle class="tip tip2" cx="260" cy="206" r="7" fill="{a}"/>'
            f'<rect x="148" y="235" width="144" height="118" rx="26" fill="{t["robot_fill"]}" stroke="{a}" stroke-width="4"/>'
            f'<ellipse class="blink" cx="192" cy="285" rx="13" ry="15" fill="{a}" fill-opacity="0.14"/><ellipse class="blink" cx="248" cy="285" rx="13" ry="15" fill="{a}" fill-opacity="0.14"/>'
            f'<circle class="blink look" cx="192" cy="287" r="6.5" fill="{a}"/><circle class="blink look" cx="248" cy="287" r="6.5" fill="{a}"/>'
            f'<path d="M 204 318 Q 220 334 236 318" fill="none" stroke="{a}" stroke-width="4" stroke-linecap="round"/>'
            '</g></g>')


STYLE = """
.halo{transform-box:fill-box;transform-origin:center;animation:halo 9s ease-in-out infinite}
@keyframes halo{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.07);opacity:.8}}
.orbit{stroke-dasharray:2 10;animation:flow 14s linear infinite}
@keyframes flow{to{stroke-dashoffset:-240}}
.bot{transform-origin:220px 294px;animation:tilt 11s ease-in-out infinite}
@keyframes tilt{0%,100%{transform:rotate(0)}12%{transform:rotate(-8deg)}26%{transform:rotate(0)}40%{transform:rotate(4deg)}55%{transform:rotate(0)}70%{transform:rotate(7deg)}85%{transform:rotate(-3deg)}}
.tip{animation:tip 1.4s ease-in-out infinite}.tip2{animation-delay:.4s}
@keyframes tip{0%,100%{opacity:.5}50%{opacity:1}}
.blink{transform-box:fill-box;transform-origin:center;animation:blink 4s ease-in-out infinite}
@keyframes blink{0%,92%,100%{transform:scaleY(1)}95%,97%{transform:scaleY(.15)}}
.zone{transform-box:fill-box;transform-origin:center;animation:breathe 4s ease-in-out infinite}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.025)}}
.r-node{transform-box:fill-box;transform-origin:center;opacity:.9;animation:node 4.2s ease-in-out infinite}
.r-dead{opacity:.32;animation-name:dead}
@keyframes node{0%,12%,40%,100%{transform:scale(1)}24%{transform:scale(1.45)}}
@keyframes dead{0%,12%,100%{transform:scale(1);opacity:.32}24%{transform:scale(1.3);opacity:.7}}
.r-edge{stroke-width:2;stroke-opacity:.45}
.r-sig{stroke-width:3;stroke-dasharray:7 60;animation:sig 4.2s linear infinite}
@keyframes sig{from{stroke-dashoffset:67}to{stroke-dashoffset:0}}
.r-goal{transform-box:fill-box;transform-origin:center;opacity:.75;animation:goal 4.2s ease-out infinite}
@keyframes goal{0%,60%,100%{transform:scale(1);opacity:.75}72%{transform:scale(1.25);opacity:.25}}
.r-check{transform-box:fill-box;transform-origin:center;animation:check 4.2s ease-out infinite}
@keyframes check{0%,58%,100%{transform:scale(1)}66%{transform:scale(1.25)}}
.e-cube{animation:float 3.2s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
.e-cone{transform-origin:0 0;animation:sweep 3s ease-in-out infinite}
@keyframes sweep{0%,100%{transform:rotate(-14deg)}50%{transform:rotate(14deg)}}
.e-halo{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-in-out infinite}
@keyframes pulse{0%,100%{transform:scale(1);opacity:.4}50%{transform:scale(1.6);opacity:.08}}
.a-line{transform-box:fill-box;transform-origin:left center;animation:type 4.5s ease-out infinite}
@keyframes type{0%,4%{transform:scaleX(0)}20%,85%{transform:scaleX(1)}100%{transform:scaleX(0)}}
.a-cursor{animation:cur 1s step-end infinite}
@keyframes cur{0%,50%{opacity:1}51%,100%{opacity:0}}
.a-app{animation:app 2.4s ease-in-out infinite}
@keyframes app{0%,100%{fill-opacity:.85}50%{fill-opacity:.45}}
.a-tap{transform-box:fill-box;transform-origin:center;animation:tap 2.4s ease-out infinite}
@keyframes tap{0%{transform:scale(.3);opacity:.9}60%,100%{transform:scale(1.9);opacity:0}}
.l-bar{transform-box:fill-box;transform-origin:center bottom;animation:grow 4.8s ease-out infinite}
@keyframes grow{0%,4%{transform:scaleY(.12)}26%,86%{transform:scaleY(1)}100%{transform:scaleY(.12)}}
.l-trend{stroke-dashoffset:0;animation:trend 2.4s linear infinite}
@keyframes trend{to{stroke-dashoffset:-16}}
.l-loop{transform-origin:0 0;animation:spin 6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.l-sprout{transform-origin:0 12px;animation:sprout 4.8s ease-in-out infinite}
@keyframes sprout{0%,100%{transform:scale(.85)}50%{transform:scale(1.08)}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


def build(theme):
    t = THEMES[theme]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
         f'<style>{STYLE}</style>',
         '<defs>',
         f'<radialGradient id="glow"><stop offset="0" stop-color="{t["halo"]}" stop-opacity="0.22"/><stop offset="1" stop-color="{t["halo"]}" stop-opacity="0"/></radialGradient>',
         '</defs>',
         f'<rect width="{W}" height="{H}" rx="20" fill="{t["bg"]}"/>',
         f'<circle class="halo" cx="{CX}" cy="{CY}" r="300" fill="url(#glow)"/>']
    # clockwise orbit (starts at R, passes E, A, L)
    orbit = f'M {CX - RX} {CY} A {RX} {RY} 0 1 1 {CX + RX} {CY} A {RX} {RY} 0 1 1 {CX - RX} {CY}'
    o.append(f'<path class="orbit" d="{orbit}" fill="none" stroke="{t["orbit"]}" stroke-width="2.2" stroke-linecap="round"/>')
    for k, delay in zip('REAL', (-1.75, -5.25, -8.75, -12.25)):
        o.append(f'<circle r="5.5" fill="{col(k, theme)}"><animateMotion dur="14s" begin="{delay}s" repeatCount="indefinite" path="{orbit}"/></circle>')
    # hand-off labels on the orbit
    import math
    for text, deg, anchor in FLOW:
        th = math.radians(deg)
        x, y = CX + RX * 1.08 * math.cos(th), CY + RY * 1.1 * math.sin(th)
        o.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-size="15" font-style="italic" fill="{t["soft"]}">{escape(text)}</text>')
    # spokes: the agent exchanges with every pillar
    for k, (zx, zy) in ZONES.items():
        dx, dy = zx - CX, zy - CY
        import math as m
        d = m.hypot(dx, dy)
        sx, sy = CX + dx / d * 108, CY + dy / d * (172 if k == 'E' else 96)
        ex, ey = zx - dx / d * 118, zy - dy / d * 84
        p = f'M {sx:.0f} {sy:.0f} L {ex:.0f} {ey:.0f}'
        c = col(k, theme)
        o.append(f'<path d="{p}" stroke="{c}" stroke-opacity="0.35" stroke-width="1.4" stroke-dasharray="3 5" fill="none"/>')
        o.append(f'<circle r="3.6" fill="{c}"><animateMotion dur="3s" repeatCount="indefinite" path="{p}"/></circle>')
        o.append(f'<circle r="3.6" fill="{c}" opacity="0.5"><animateMotion dur="3s" begin="-1.5s" repeatCount="indefinite" keyPoints="1;0" keyTimes="0;1" calcMode="linear" path="{p}"/></circle>')
    # zones
    scenes = {'R': scene_reasoning, 'E': scene_embodied, 'L': scene_lifelong}
    for k, (zx, zy) in ZONES.items():
        name, phrase, _, _ = PILLAR[k]
        c = col(k, theme)
        o.append(f'<rect x="{zx - 128}" y="{zy - 82}" width="256" height="164" rx="22" fill="{t["card"]}" stroke="{c}" stroke-opacity="0.35" stroke-width="1.4"/>')
        body = scene_agentic(c, t) if k == 'A' else scenes[k](c)
        o.append(f'<g transform="translate({zx},{zy})"><g class="zone">{body}</g></g>')
        # title block: above for E, below for L, above the card for R and A
        ty = {'E': zy - 104, 'L': zy + 112, 'R': zy - 106, 'A': zy - 106}[k]
        o.append(f'<circle cx="{zx - 74}" cy="{ty - 7}" r="15" fill="{c}"/>')
        o.append(f'<text x="{zx - 74}" y="{ty - 1}" text-anchor="middle" font-size="16" font-weight="800" fill="{'#FFFFFF' if theme == 'light' else '#0D1117'}">{k}</text>')
        o.append(f'<text x="{zx - 51}" y="{ty - 1}" font-size="19" font-weight="750" fill="{t["ink"]}">{name}<tspan font-size="14.5" font-weight="400" fill="{t["soft"]}" dx="8">{phrase}</tspan></text>')
    # robot at the centre
    o.append(f'<g transform="translate({CX},{CY + 8})">{robot(t)}</g>')
    o.append('</svg>')
    return '\n'.join(o)


OUT = os.environ.get('MAP_OUT', 'profile/assets')
for th in THEMES:
    open(os.path.join(OUT, f'research-map-{th}.svg'), 'w').write(build(th))
print('ok')
