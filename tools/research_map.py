"""Animated REAL research map in the website's visual language (CSS + SMIL only, so it plays inside a GitHub README).

Run from the repository root:  python3 tools/research_map.py
Writes profile/assets/research-map-light.svg and research-map-dark.svg.
"""
import math
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
EAGLE = 'M44.1474 66.4569L39.1672 58.8578C40.6965 58.0705 40.5071 55.6155 39.197 55.4113C37.7385 55.1828 36.5775 55.1126 35.5542 52.8197H37.9267L37.1984 50.831C34.4838 51.0694 33.93 50.315 32.6429 48.1947L36.0336 48.0786L35.3481 46.3481C31.6532 46.5195 30.6784 45.6136 29.7558 43.5082L34.061 43.3573L33.129 41.2984C28.7201 41.4214 27.7869 41.2966 26.1701 38.3151L31.647 38.2884L30.8746 36.327C25.8826 36.5424 24.6359 36.0538 23.2227 33.5572L34.4435 33.2734C36.0789 33.2318 37.9459 34.3463 38.6339 35.8296L39.9831 38.741L41.403 33.8409C42.1351 31.3164 47.6523 32.2316 49.428 33.9117L46.0907 35.1187L47.7237 39.0949C48.9071 36.3257 50.3569 33.2722 53.4762 33.2722H64.484C63.6371 35.7042 61.5925 36.9168 57.1482 36.1301L56.3671 38.189L61.8564 38.1723C60.5426 41.2351 59.0847 41.6201 55.0018 41.1556L54.1493 43.2145L58.5191 43.3567C57.6784 45.2976 56.1566 46.458 52.7833 46.0545L52.073 48.0593L55.5525 48.0432C54.5553 50.482 53.9115 51.0265 50.74 50.8837L50.0129 52.8718L52.5194 52.8811C51.4658 55.004 51.1535 55.256 48.9046 55.4554C47.5678 55.5739 46.9718 57.7141 48.7519 58.9826L44.1474 66.4569Z'  # ZJU Qiushi eagle, as on the website

W, H = 1120, 706
CX, CY = 560, 366                 # robot / orbit centre
RX, RY = 320, 226                 # orbit radii
ZONES = {                         # centre of each illustration
    'R': (240, 366), 'E': (560, 133), 'L': (880, 366), 'A': (560, 584),
}
PILLAR = {
    'R': ('Reasoning', 'reasons reliably', '#004EA2', '#6FA0E0'),
    'E': ('Embodied', 'explores the world', '#13808C', '#6CC3CC'),
    'A': ('Agentic', 'acts autonomously', '#4A6FA5', '#93A9D1'),
    'L': ('Lifelong', 'learns continuously', '#2E7D5B', '#7DC4A0'),
}
TITLE_DY = {'R': -94, 'E': -92, 'L': -94, 'A': 100}   # title baseline relative to the card centre
CENTRE = {'R': (-4, 0), 'E': (0, -6), 'A': (7, 2), 'L': (8, 15)}   # nudge each scene to its card centre
FLOW = [  # (from, to, label lines, position on the orbit in degrees, anchor)
    ('R', 'E', ('reasoning becomes', 'physical action'), 225, 'end'),
    ('E', 'L', ('physical action', 'yields experience'), 315, 'start'),
    ('R', 'A', ('reasoning becomes', 'digital action'), 135, 'end'),
    ('A', 'L', ('digital action', 'yields experience'), 45, 'start'),
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


def _cube(c, x, y, k=1.0):
    pts = lambda ps: ' '.join(f'{x + px * k:.1f},{y + py * k:.1f}' for px, py in ps)
    return (f'<polygon points="{pts([(0, -22), (22, -11), (0, 0), (-22, -11)])}" fill="{c}" fill-opacity="0.9"/>'
            f'<polygon points="{pts([(-22, -11), (0, 0), (0, 24), (-22, 13)])}" fill="{c}" fill-opacity="0.55"/>'
            f'<polygon points="{pts([(0, 0), (22, -11), (22, 13), (0, 24)])}" fill="{c}" fill-opacity="0.75"/>')


def _cylinder(c, x, y, k=1.0):
    rx, h, ry = 14 * k, 30 * k, 6 * k
    return (f'<rect x="{x - rx:.1f}" y="{y - h:.1f}" width="{2 * rx:.1f}" height="{h:.1f}" fill="{c}" fill-opacity="0.6"/>'
            f'<ellipse cx="{x}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{c}" fill-opacity="0.6"/>'
            f'<ellipse cx="{x}" cy="{y - h:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{c}" fill-opacity="0.9"/>')


def _sphere(c, x, y, k=1.0):
    r = 14 * k
    return (f'<circle cx="{x}" cy="{y - r:.1f}" r="{r:.1f}" fill="{c}" fill-opacity="0.75"/>'
            f'<circle cx="{x - r * 0.35:.1f}" cy="{y - r * 1.35:.1f}" r="{r * 0.32:.1f}" fill="#FFFFFF" fill-opacity="0.45"/>')


def _row(c, xs, y, k):
    # the same three objects, left to right: cylinder, cube, sphere
    return _cylinder(c, xs[0], y, k) + _cube(c, xs[1], y - 24 * k, k) + _sphere(c, xs[2], y, k)


def scene_embodied(c):
    # left: a robot walks along the front of the scene; right: exactly what it sees, on the same timeline
    W2, H2 = 56, 46
    o = [f'<defs><clipPath id="e3"><rect x="{-W2}" y="{-H2}" width="{2 * W2}" height="{2 * H2}" rx="9"/></clipPath>'
         f'<clipPath id="e1"><rect x="{-W2}" y="{-H2}" width="{2 * W2}" height="{2 * H2}" rx="9"/></clipPath></defs>']
    # ---- third person
    floor = [f'<polygon points="0,-24 56,4 0,32 -56,4" fill="{c}" fill-opacity="0.14"/>']
    for k in range(1, 4):
        t = k / 4
        floor.append(f'<line x1="{-56 + 56 * t:.1f}" y1="{4 - 28 * t:.1f}" x2="{56 * t:.1f}" y2="{32 - 28 * t:.1f}" stroke="{c}" stroke-opacity="0.22" stroke-dasharray="2 3"/>')
        floor.append(f'<line x1="{-56 + 56 * t:.1f}" y1="{4 + 28 * t:.1f}" x2="{56 * t:.1f}" y2="{-24 + 28 * t:.1f}" stroke="{c}" stroke-opacity="0.22" stroke-dasharray="2 3"/>')
    walker = ('<g>'
              f'<path d="M 0 -12 L -14 -40 A 30 30 0 0 1 14 -40 Z" fill="{c}" fill-opacity="0.2"/>'
              f'<ellipse cx="0" cy="2" rx="5" ry="2" fill="{c}" fill-opacity="0.3"/>'
              f'<rect x="-4" y="-9" width="8" height="10" rx="2.5" fill="{c}"/>'
              f'<circle cx="0" cy="-12" r="3.6" fill="{c}"/>'
              '<animateMotion path="M -26 0 Q 0 -16 26 0" dur="28s" repeatCount="indefinite" keyPoints="0;1;0" keyTimes="0;0.5;1" '
              'calcMode="spline" keySplines=".42 0 .58 1;.42 0 .58 1"/>'
              '</g>')
    third = (''.join(floor)
             + f'<path d="M -26 22 Q 0 6 26 22" fill="none" stroke="{c}" stroke-opacity="0.35" stroke-dasharray="3 3"/>'
             + _row(c, (-26, 0, 26), 6, 0.5)
             + f'<g transform="translate(0,22)">{walker}</g>')
    o.append('<g transform="translate(-62,0)">'
             f'<g clip-path="url(#e3)"><g transform="translate(0,4)">{third}</g></g>'
             f'<text x="0" y="{H2 + 14}" text-anchor="middle" font-size="9.5" font-weight="600" letter-spacing=".6" fill="{c}" fill-opacity="0.85">third-person</text>'
             '</g>')
    # ---- first person: the same row, seen from the robot, panning with its walk
    far = (f'<line x1="-220" y1="-34" x2="220" y2="-34" stroke="{c}" stroke-opacity="0.25" stroke-width="1.2"/>'
           f'<path d="M -220 -34 L -170 -54 L -120 -40 L -70 -60 L -20 -38 L 30 -54 L 80 -38 L 130 -58 L 180 -40 L 220 -34 Z" fill="{c}" fill-opacity="0.10"/>')
    ground = [f'<rect x="-240" y="-34" width="480" height="140" fill="{c}" fill-opacity="0.11"/>']
    for gx in range(-240, 241, 40):
        ground.append(f'<line x1="{gx}" y1="-34" x2="{gx * 1.8}" y2="106" stroke="{c}" stroke-opacity="0.2" stroke-dasharray="2 4"/>')
    for gy in (-10, 22, 64):
        ground.append(f'<line x1="-240" y1="{gy}" x2="240" y2="{gy}" stroke="{c}" stroke-opacity="0.18" stroke-dasharray="2 4"/>')
    near = ''.join(ground) + _row(c, (-80, 0, 80), 34, 1.25)
    hud = (''.join(f'<path d="M {sx * 48} {sy * 28} L {sx * 48} {sy * 38} L {sx * 38} {sy * 38}" '
                   f'stroke="{c}" stroke-width="2" fill="none" stroke-linecap="round"/>'
                   for sx in (-1, 1) for sy in (-1, 1))
           + f'<rect class="e-focus" x="-9" y="-8" width="18" height="16" rx="2.5" fill="none" stroke="{c}" stroke-width="1.6"/>'
           + f'<line x1="-3.5" y1="0" x2="3.5" y2="0" stroke="{c}" stroke-width="1.2"/><line x1="0" y1="-3.5" x2="0" y2="3.5" stroke="{c}" stroke-width="1.2"/>'
           + '<circle class="e-rec" cx="-41" cy="-28" r="3" fill="#E5484D"/>'
           + f'<text x="-34" y="-25" font-size="8" font-weight="700" letter-spacing=".8" fill="{c}">REC</text>')
    o.append('<g transform="translate(62,0)">'
             f'<g clip-path="url(#e1)"><g transform="translate(0,-2) scale(0.6)"><g class="e-far">{far}</g><g class="e-zoom"><g class="e-pan">{near}</g></g></g></g>'
             + hud
             + f'<text x="0" y="{H2 + 14}" text-anchor="middle" font-size="9.5" font-weight="600" letter-spacing=".6" fill="{c}" fill-opacity="0.85">first-person</text>'
             '</g>')
    o.append(f'<line x1="0" y1="-50" x2="0" y2="62" stroke="{c}" stroke-opacity="0.25" stroke-width="1.2"/>')
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


def scene_lifelong(c, theme='light'):
    # experience bars that keep growing, a loop that keeps turning, a sprout that keeps rising
    o = []
    for i, h in enumerate([26, 40, 56, 74]):
        o.append(f'<rect class="l-bar" style="animation-delay:{0.4 * i:.2f}s" x="{-96 + 26 * i}" y="{30 - h}" width="17" height="{h}" rx="4" fill="{c}" fill-opacity="{0.35 + 0.18 * i:.2f}"/>')
    o.append(f'<line x1="-104" y1="31" x2="6" y2="31" stroke="{c}" stroke-opacity="0.35" stroke-width="1.5"/>')
    # trend arrow: colour gradient from a light mint at the start to the deep pillar green at the arrowhead
    start = '#86EFC7' if theme == 'light' else '#1F7A5C'
    end = '#047857' if theme == 'light' else '#5BF0B0'

    def mix(t):
        a = [int(start[i:i + 2], 16) for i in (1, 3, 5)]
        b = [int(end[i:i + 2], 16) for i in (1, 3, 5)]
        return '#' + ''.join(f'{round(a[j] + (b[j] - a[j]) * t):02X}' for j in range(3))

    o.append(f'<defs><linearGradient id="ltrend" gradientUnits="userSpaceOnUse" x1="-87.5" y1="-8" x2="-9.5" y2="-56">'
             f'<stop offset="0" stop-color="{start}"/><stop offset="1" stop-color="{end}"/></linearGradient></defs>')
    pts = [(-87.5, -8), (-61.5, -22), (-35.5, -38), (-9.5, -56)]
    o.append('<path class="l-trend" d="M -87.5 -8 C -78 -12, -70 -17, -61.5 -22 S -44 -32, -35.5 -38 S -18 -50, -9.5 -56" '
             'fill="none" stroke="url(#ltrend)" stroke-width="2.6" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(pts):
        o.append(f'<circle class="l-dot" style="animation-delay:{0.4 * i:.2f}s" cx="{x}" cy="{y}" r="3.4" fill="{mix(i / 3)}"/>')
    o.append(f'<path class="l-head" d="M -15.5 -57 L -6 -60 L -9.5 -50.5" fill="none" stroke="{end}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<g transform="translate(62,-6)"><g class="l-loop">'
             f'<path d="M 26 0 A 26 26 0 1 1 18.4 -18.4" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round"/>'
             f'<path d="M 18.4 -18.4 L 10 -24 M 18.4 -18.4 L 24 -10" stroke="{c}" stroke-width="3" stroke-linecap="round"/></g>'
             f'<g class="l-sprout"><path d="M 0 12 L 0 -4" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/>'
             f'<path d="M 0 -2 C -10 -4, -12 -12, -10 -16 C -4 -14, 0 -10, 0 -2 Z" fill="{c}"/>'
             f'<path d="M 0 -4 C 9 -7, 12 -15, 10 -19 C 3 -17, 0 -12, 0 -4 Z" fill="{c}" fill-opacity="0.75"/></g></g>')
    return ''.join(o)


def robot(t):
    # a flat, friendly robot in ZJU blue: light face plate, dark eyes, soft cheeks, mint antenna (REAL logo dot), Qiushi eagle above
    body, face, eye = '#004EA2', '#F4F7FC', '#1B2A4A'
    return (
        '<defs>'
        '<radialGradient id="tipg"><stop offset="0" stop-color="#19D3A7" stop-opacity=".55"/><stop offset="1" stop-color="#19D3A7" stop-opacity="0"/></radialGradient>'
        '</defs>'
        f'<ellipse class="shadow" cx="0" cy="80" rx="48" ry="7" fill="{t["ink"]}" fill-opacity="0.10"/>'
        '<g class="botf">'
        f'<g transform="translate(-198,-274.6) scale(0.9)"><g transform="translate(175, 118) scale(1.0225)"><path d="{EAGLE}" fill="{t["eagle"]}" fill-rule="evenodd"/></g></g>'
        f'<line x1="0" y1="-62" x2="0" y2="-80" stroke="{body}" stroke-width="5" stroke-linecap="round"/>'
        '<circle class="tip" cx="0" cy="-84" r="16" fill="url(#tipg)"/>'
        '<circle cx="0" cy="-84" r="7" fill="#19D3A7"/>'
        f'<rect x="-86" y="-22" width="16" height="40" rx="8" fill="{body}"/>'
        f'<rect x="70" y="-22" width="16" height="40" rx="8" fill="{body}"/>'
        f'<rect x="-74" y="-62" width="148" height="122" rx="30" fill="{body}"/>'
        f'<rect x="-58" y="-44" width="116" height="86" rx="22" fill="{face}"/>'
        f'<circle class="blink" cx="-22" cy="-6" r="9" fill="{eye}"/>'
        f'<circle class="blink" cx="22" cy="-6" r="9" fill="{eye}"/>'
        '<circle cx="-36" cy="12" r="6" fill="#FF9DB0" fill-opacity="0.5"/>'
        '<circle cx="36" cy="12" r="6" fill="#FF9DB0" fill-opacity="0.5"/>'
        f'<path d="M -12 14 Q 0 24 12 14" fill="none" stroke="{eye}" stroke-width="3.6" stroke-linecap="round"/>'
        '</g>')


STYLE = """
.halo{transform-box:fill-box;transform-origin:center;animation:halo 9s ease-in-out infinite}
@keyframes halo{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.07);opacity:.8}}
.orbit{stroke-dasharray:2 10;animation:flow 14s linear infinite}
@keyframes flow{to{stroke-dashoffset:-240}}
.botf{animation:hover 4s ease-in-out infinite}
@keyframes hover{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
.shadow{transform-box:fill-box;transform-origin:center;animation:shade 4s ease-in-out infinite}
@keyframes shade{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(.86);opacity:.7}}
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
.e-walk{animation:walk 14s ease-in-out infinite alternate}
@keyframes walk{from{transform:translateX(-26px)}to{transform:translateX(26px)}}
.e-pan{animation:pan 14s ease-in-out infinite alternate}
.e-zoom{animation:zoom 14s ease-in-out infinite alternate}
@keyframes zoom{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(6px) scale(1.12)}}
@keyframes pan{from{transform:translateX(80px)}to{transform:translateX(-80px)}}
.e-far{animation:drift 14s ease-in-out infinite alternate}
@keyframes drift{from{transform:translateX(26px)}to{transform:translateX(-26px)}}
.e-focus{transform-box:fill-box;transform-origin:center;animation:focus 4s ease-in-out infinite}
@keyframes focus{0%,100%{transform:scale(1);opacity:.9}50%{transform:scale(.8);opacity:.55}}
.e-rec{animation:rec 1.2s step-end infinite}
@keyframes rec{0%,50%{opacity:1}51%,100%{opacity:.15}}
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
.l-trend{stroke-dasharray:110;stroke-dashoffset:110;animation:draw 4.8s ease-out infinite}
@keyframes draw{0%,22%{stroke-dashoffset:110}48%,86%{stroke-dashoffset:0}100%{stroke-dashoffset:110}}
.l-head{opacity:0;animation:head 4.8s ease-out infinite}
@keyframes head{0%,44%{opacity:0}50%,86%{opacity:1}100%{opacity:0}}
.l-dot{transform-box:fill-box;transform-origin:center;opacity:0;animation:dot 4.8s ease-out infinite}
@keyframes dot{0%,20%{opacity:0;transform:scale(.4)}30%,86%{opacity:1;transform:scale(1)}100%{opacity:0}}
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
         f'<circle class="halo" cx="{CX}" cy="{CY}" r="225" fill="url(#glow)"/>']
    # two paths out of R (physical via E, digital via A) converge on L
    deg = {'R': 180, 'E': 270, 'L': 360, 'A': 90}
    pt = lambda a: (CX + RX * math.cos(math.radians(a)), CY + RY * math.sin(math.radians(a)))
    holes = []
    for k, (zx, zy) in ZONES.items():
        name, phrase = PILLAR[k][0], PILLAR[k][1]
        ty = zy + TITLE_DY[k]
        tw = len(name) * 11.2 + 8 + len(phrase) * 7.7
        holes.append(f'<rect x="{zx - 100}" y="{ty - 30}" width="{tw + 60:.0f}" height="{46 if k == "A" else 56}" rx="12" fill="#000"/>')
    o.append(f'<mask id="titles" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
             f'<rect width="{W}" height="{H}" fill="#fff"/>' + ''.join(holes) + '</mask>')
    defs, paths, marks = [], [], []
    for n, (a, b, lines, mid, anchor) in enumerate(FLOW):
        a0, a1 = deg[a], deg[b]
        if a1 - a0 > 180:                      # take the short way round (A at 90 deg reaches L at 0 deg)
            a1 -= 360
        (x0, y0), (x1, y1) = pt(a0), pt(a1)
        sweep = 1 if a1 > a0 else 0
        d = f'M {x0:.1f} {y0:.1f} A {RX} {RY} 0 0 {sweep} {x1:.1f} {y1:.1f}'
        defs.append(f'<linearGradient id="f{n}" gradientUnits="userSpaceOnUse" x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}">'
                    f'<stop offset="0.15" stop-color="{col(a, theme)}"/><stop offset="0.85" stop-color="{col(b, theme)}"/></linearGradient>')
        paths.append(f'<path class="orbit" d="{d}" fill="none" stroke="url(#f{n})" stroke-width="2.4" stroke-linecap="round"/>')
        for delay in (0, -2.5):
            paths.append(f'<circle r="5" fill="{col(a, theme)}"><animateMotion dur="5s" begin="{delay}s" repeatCount="indefinite" path="{d}"/></circle>')
        # chevron at the midpoint, pointing along the flow
        th = math.radians(mid)
        mx, my = pt(mid)
        sgn = 1 if sweep else -1
        ang = math.degrees(math.atan2(sgn * RY * math.cos(th), -sgn * RX * math.sin(th)))
        cm = col(b, theme) if b == 'L' else col(a, theme)
        marks.append(f'<path d="M -5 -6 L 3 0 L -5 6" transform="translate({mx:.1f},{my:.1f}) rotate({ang:.1f})" fill="none" stroke="{cm}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
        lx, ly = CX + RX * 1.08 * math.cos(th), CY + RY * 1.1 * math.sin(th)
        ly += -18 if my < CY else 6
        lx += (-1 if anchor == 'end' else 1) * max(map(len, lines)) * 7.3 / 2   # keep the block in place, centre its lines
        marks.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="middle" font-size="15" font-style="italic" fill="{t["soft"]}">'
                     + ''.join(f'<tspan x="{lx:.0f}" dy="{0 if i == 0 else 19}">{escape(line)}</tspan>' for i, line in enumerate(lines)) + '</text>')
    o.append('<defs>' + ''.join(defs) + '</defs>')
    o.append('<g mask="url(#titles)">' + ''.join(paths) + '</g>')
    o.extend(marks)
    # spokes: the agent exchanges with every pillar
    for k, (zx, zy) in ZONES.items():
        dx, dy = zx - CX, zy - CY
        d = math.hypot(dx, dy)
        sx, sy = CX + dx / d * 70, CY + dy / d * (88 if k == 'E' else 66)
        ex, ey = zx - dx / d * 118, zy - dy / d * (76 if k == 'E' else 72)
        p = f'M {sx:.0f} {sy:.0f} L {ex:.0f} {ey:.0f}'
        c = col(k, theme)
        o.append(f'<path d="{p}" stroke="{c}" stroke-opacity="0.35" stroke-width="1.4" stroke-dasharray="3 5" fill="none"/>')
    # zones
    scenes = {'R': scene_reasoning, 'E': scene_embodied, 'L': scene_lifelong}
    for k, (zx, zy) in ZONES.items():
        name, phrase, _, _ = PILLAR[k]
        c = col(k, theme)
        o.append(f'<rect x="{zx - 128}" y="{zy - 70}" width="256" height="140" rx="20" fill="{t["card"]}" stroke="{c}" stroke-opacity="0.35" stroke-width="1.4"/>')
        body = scene_agentic(c, t) if k == 'A' else (scene_lifelong(c, theme) if k == 'L' else scenes[k](c))
        ox, oy = CENTRE[k]
        o.append(f'<g transform="translate({zx + ox},{zy + oy})"><g class="zone">{body}</g></g>')
        # title block: below the card for A, above it for R, E and L
        ty = zy + TITLE_DY[k]
        o.append(f'<circle cx="{zx - 74}" cy="{ty - 7}" r="15" fill="{c}"/>')
        o.append(f'<text x="{zx - 74}" y="{ty - 1}" text-anchor="middle" font-size="16" font-weight="800" fill="{'#FFFFFF' if theme == 'light' else '#0D1117'}">{k}</text>')
        o.append(f'<text x="{zx - 51}" y="{ty - 1}" font-size="19" font-weight="750" fill="{t["ink"]}">{name}<tspan font-size="14.5" font-weight="400" fill="{t["soft"]}" dx="8">{phrase}</tspan></text>')
    # robot at the centre
    o.append(f'<g transform="translate({CX},{CY + 4}) scale(0.62)">{robot(t)}</g>')
    o.append('</svg>')
    return '\n'.join(o)


OUT = os.environ.get('MAP_OUT', 'profile/assets')
for th in THEMES:
    open(os.path.join(OUT, f'research-map-{th}.svg'), 'w').write(build(th))
print('ok')
