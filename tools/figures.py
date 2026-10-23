"""Banner and research-map SVGs for the ZJU-REAL GitHub profile, in light and dark variants.

Edit BANDS / LINKS / ENGINE below when the research map changes, then run:
    python3 tools/figures.py
Requires Pillow (for text-width measurement) and macOS Helvetica; any similar font path works.
"""
import base64, math, os
from xml.sax.saxutils import escape
from PIL import ImageFont

OUT = 'profile/assets'   # run from the repository root: python3 tools/figures.py
os.makedirs(OUT, exist_ok=True)
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
_HV = '/System/Library/Fonts/Helvetica.ttc'


def tw(text, size, bold=False):
    """Text width estimate (Helvetica metrics + margin for other system fonts)."""
    f = ImageFont.truetype(_HV, round(size), index=1 if bold else 0)
    return f.getlength(text) * 1.06


THEMES = {
    'light': dict(bg0='#F7FAFF', bg1='#EDF3FF', dot='#C9D6EE', ink='#0F172A', soft='#475569', mute='#64748B',
                  accent='#1D4ED8', panel='#FFFFFF', panel_line='#DCE5F3', chip='#FFFFFF', glow='0.55',
                  spine='#F1F5FB', arrow='#94A3B8'),
    'dark': dict(bg0='#0D1117', bg1='#101A2E', dot='#1E2A40', ink='#E6EDF3', soft='#B6C2D2', mute='#8B98AB',
                 accent='#7AA7FF', panel='#121A27', panel_line='#24324A', chip='#172133', glow='0.35',
                 spine='#111A29', arrow='#5B6B85'),
}
LAYER = {  # brand-derived hues per pillar
    'R': ('#004EA2', '#D6E4F5', '#002B5C'),
    'E': ('#13808C', '#D2EDEF', '#0A454C'),
    'A': ('#4A6FA5', '#E0EAF7', '#1E3A5F'),
    'L': ('#2E7D5B', '#D5ECDF', '#164030'),
}


# --------------------------------------------------------------------------- banner
def banner(theme):
    t = THEMES[theme]
    W, H = 1280, 360
    wm = base64.b64encode(open('tools/real-wordmark.png', 'rb').read()).decode()
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs>',
         f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg0"]}"/><stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>',
         f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t["dot"]}"/></pattern>',
         f'<radialGradient id="g1"><stop offset="0" stop-color="#126DFF" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="#126DFF" stop-opacity="0"/></radialGradient>',
         f'<radialGradient id="g2"><stop offset="0" stop-color="#19D3A7" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="#19D3A7" stop-opacity="0"/></radialGradient>',
         '<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="0.55" stop-color="#000" stop-opacity="1"/></linearGradient>',
         f'<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>',
         '</defs>',
         f'<rect width="{W}" height="{H}" rx="22" fill="url(#bg)"/>',
         f'<rect width="{W}" height="{H}" rx="22" fill="url(#dots)" mask="url(#m)"/>',
         '<circle cx="1040" cy="70" r="260" fill="url(#g1)"/>',
         '<circle cx="880" cy="330" r="210" fill="url(#g2)"/>',
         f'<image x="70" y="78" width="383" height="88" xlink:href="data:image/png;base64,{wm}"/>',
         f'<text x="72" y="222" font-family="{FONT}" font-size="25" font-weight="650" fill="{t["accent"]}">'
         'Reasoning · Embodied · Agentic · Lifelong-learning AI</text>',
         f'<text x="72" y="262" font-family="{FONT}" font-size="20" fill="{t["soft"]}">'
         'Toward AI that thinks, acts, and grows in the real world.</text>',
         f'<text x="72" y="312" font-family="{FONT}" font-size="13" letter-spacing="3" font-weight="600" fill="{t["mute"]}">'
         'ZHEJIANG UNIVERSITY</text>']

    o.append(tower(theme))
    o.append('</svg>')
    return '\n'.join(o)


# --------------------------------------------------------------------------- 灿若星辰 light tower (ZJU Zijingang)
def _icosphere(freq=2):
    p = (1 + 5 ** .5) / 2
    V = [(-1, p, 0), (1, p, 0), (-1, -p, 0), (1, -p, 0), (0, -1, p), (0, 1, p), (0, -1, -p), (0, 1, -p),
         (p, 0, -1), (p, 0, 1), (-p, 0, -1), (-p, 0, 1)]
    F = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
         (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    norm = lambda v: tuple(c / math.sqrt(sum(x * x for x in v)) for c in v)
    V = [norm(v) for v in V]
    for _ in range(freq):
        cache, nf = {}, []
        def mid(a, b):
            key = (min(a, b), max(a, b))
            if key not in cache:
                V.append(norm(tuple((V[a][i] + V[b][i]) / 2 for i in range(3))))
                cache[key] = len(V) - 1
            return cache[key]
        for a, b, c in F:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            nf += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
        F = nf
    E = set()
    for a, b, c in F:
        for x, y in ((a, b), (b, c), (c, a)):
            E.add((min(x, y), max(x, y)))
    return V, E


TOWER = {  # light: blue line art; dark: the tower lit at night
    'light': dict(bulb='#FFFFFF', ring='#2F7FD6', rod='#004EA2', rod_front=.42, rod_back=.13, glow='#9CC3F5', glow_op=.45, pole='#004EA2'),
    'dark': dict(bulb='#FFF6DC', ring='#FFC94D', rod='#C9A866', rod_front=.55, rod_back=.18, glow='#FFD978', glow_op=.30, pole='#C9D6EA'),
}


def tower(theme, cx=1012, base=372, length=212, rad=96, tilt=7):
    """The tower rising from below the banner: pole into a geodesic sphere of lamps, collar at the entry, spire fading out."""
    c = TOWER[theme]
    V, E = _icosphere(2)
    t = math.radians(-16)                                  # looking slightly up at the sphere
    P = []
    for x, y, z in V:
        y2, z2 = y * math.cos(t) - z * math.sin(t), y * math.sin(t) + z * math.cos(t)
        P.append((x * rad, -length - y2 * rad, z2))
    cy = -length
    ye, yx = cy + rad * math.cos(t), cy - rad * math.cos(t)
    tip = yx - rad * 1.4
    o = [f'<defs>'
         f'<linearGradient id="tw-pole" x1="0" x2="1"><stop offset="0" stop-color="{c["pole"]}" stop-opacity=".55"/>'
         f'<stop offset=".45" stop-color="{c["pole"]}" stop-opacity=".22"/><stop offset="1" stop-color="{c["pole"]}" stop-opacity=".6"/></linearGradient>'
         f'<linearGradient id="tw-col" gradientUnits="userSpaceOnUse" x1="0" y1="{ye:.1f}" x2="0" y2="{yx:.1f}">'
         f'<stop offset="0" stop-color="{c["ring"]}" stop-opacity=".8"/><stop offset=".22" stop-color="{c["pole"]}" stop-opacity=".2"/>'
         f'<stop offset=".5" stop-color="{c["pole"]}" stop-opacity=".08"/><stop offset=".78" stop-color="{c["pole"]}" stop-opacity=".2"/>'
         f'<stop offset="1" stop-color="{c["ring"]}" stop-opacity=".8"/></linearGradient>'
         f'<linearGradient id="tw-spire" gradientUnits="userSpaceOnUse" x1="0" y1="{yx:.1f}" x2="0" y2="{tip:.1f}">'
         f'<stop offset="0" stop-color="{c["ring"]}" stop-opacity=".85"/><stop offset=".4" stop-color="{c["pole"]}" stop-opacity=".45"/>'
         f'<stop offset="1" stop-color="{c["pole"]}" stop-opacity="0"/></linearGradient>'
         f'<radialGradient id="tw-glow"><stop offset="0" stop-color="{c["glow"]}" stop-opacity="{c["glow_op"]}"/>'
         f'<stop offset=".65" stop-color="{c["glow"]}" stop-opacity="{c["glow_op"] / 4:.2f}"/><stop offset="1" stop-color="{c["glow"]}" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="tw-spot"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="{c["glow"]}" stop-opacity=".9"/>'
         f'<stop offset="1" stop-color="{c["glow"]}" stop-opacity="0"/></radialGradient>'
         f'</defs>',
         '<style>.tw-l{animation:tw 3.2s ease-in-out infinite}@keyframes tw{50%{opacity:.35}}'
         '@media (prefers-reduced-motion: reduce){.tw-l{animation:none}}</style>',
         f'<g transform="translate({cx},{base}) rotate({tilt})">',
         f'<circle cx="0" cy="{cy}" r="{rad * 1.45:.0f}" fill="url(#tw-glow)"/>',
         f'<path d="M -3.6 {yx + 2:.1f} L 0 {tip:.1f} L 3.6 {yx + 2:.1f} Z" fill="url(#tw-spire)"/>']
    for i, j in E:
        if (P[i][2] + P[j][2]) / 2 <= 0:
            o.append(f'<line x1="{P[i][0]:.1f}" y1="{P[i][1]:.1f}" x2="{P[j][0]:.1f}" y2="{P[j][1]:.1f}" stroke="{c["rod"]}" '
                     f'stroke-opacity="{c["rod_back"]}" stroke-width=".9"/>')
    o.append(f'<path d="M -6 {ye:.1f} L -4.5 {yx:.1f} L 4.5 {yx:.1f} L 6 {ye:.1f} Z" fill="url(#tw-col)"/>')
    o.append(f'<ellipse cx="0" cy="{yx:.1f}" rx="16" ry="10" fill="url(#tw-spot)"/>')
    o.append(f'<path d="M -10 {ye + 4:.1f} L -19 0 L 19 0 L 10 {ye + 4:.1f} Z" fill="url(#tw-pole)"/>')
    cr = rad * .24
    o.append(f'<ellipse cx="0" cy="{ye + 2:.1f}" rx="{cr:.1f}" ry="{cr * .36:.1f}" fill="{c["rod"]}" fill-opacity=".4"/>')
    o += [f'<circle cx="{cr * .9 * math.cos(a):.1f}" cy="{ye + 2 + cr * .36 * .9 * math.sin(a):.1f}" r="1.7" fill="{c["bulb"]}" stroke="{c["ring"]}" stroke-width=".9"/>'
          for a in [k * math.pi / 8 for k in range(16)]]
    o.append(f'<ellipse cx="0" cy="{ye:.1f}" rx="20" ry="11" fill="url(#tw-spot)"/>')
    for i, j in E:
        if (P[i][2] + P[j][2]) / 2 > 0:
            o.append(f'<line x1="{P[i][0]:.1f}" y1="{P[i][1]:.1f}" x2="{P[j][0]:.1f}" y2="{P[j][1]:.1f}" stroke="{c["rod"]}" '
                     f'stroke-opacity="{c["rod_front"]}" stroke-width="1.2"/>')
    for k, (x, y, z) in sorted(enumerate(P), key=lambda e: e[1][2]):
        front = z > 0
        r = 2.2 + 1.8 * max(z, 0)
        tw = f' class="tw-l" style="animation-delay:{(k % 13) * .3:.2f}s"' if k % 5 == 0 else ''
        o.append(f'<circle{tw} cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c["bulb"]}" fill-opacity="{.95 if front else .45}" '
                 f'stroke="{c["ring"]}" stroke-width="{1.3 if front else .6}"/>')
    o.append('</g>')
    return ''.join(o)


# --------------------------------------------------------------------------- research map
BANDS = [  # top (growth) to bottom (foundation)
    ('L', 'Lifelong', 'keep growing', [[
        ('Guide', ['Agent-G²', 'BEACON']),
        ('Internalize', ['SKILL0', 'ViSkill']),
        ('Distill', ['SDAR', 'AgentOPSD']),
        ('Operate', ['HugAgentOS'], True)]]),
    ('A', 'Agentic', 'act and deliver', [
        [('Ground', ['GUI-G²', 'GUI-RCPO']), ('Act', ['UI-S1', 'UI-Copilot']),
         ('Beyond GUI', ['HybridCUA', 'ComputerSD']), ('Deploy', ['ClawGUI'], True)],
        [('Search', ['IterSynth', 'BrowserForge']), ('Build', ['Code-A1', 'PaperGym']),
         ('Discover', ['Polaris'], True), ('Create', ['Easel'], True)]]),
    ('E', 'Embodied', 'sense, predict, act', [[
        ('Perceive', ['ViewSpatial', 'SpatialLadder']),
        ('Self-evolve', ['SpatialEvo']),
        ('Predict', ['SpaceCast', 'WorldMemBench']),
        ('Act', ['VLA-Corrector', 'OmniEmbodied'])]]),
    ('R', 'Reasoning', 'think deeper', [[
        ('Longer', ['InftyThink', 'InftyThink+']),
        ('Leaner', ['Self-Braking', 'LAPO']),
        ('Verified', ['VerifyBench', 'CoVerRL'])]]),
]
BRIGHT = {'R': '#6FA0E0', 'E': '#6CC3CC', 'A': '#93A9D1', 'L': '#7DC4A0'}
ROW_TAGS = {'A': ['COMPUTER-USE AGENTS', 'RESEARCH & CREATION AGENTS']}
LINKS = {  # what each layer hands to the one above it
    ('E', 'L'): None,
    ('A', 'L'): 'every trajectory becomes experience for the next policy',
    ('E', 'A'): 'grounding in the physical world lets agents act beyond the screen',
    ('R', 'E'): 'reasoning grounded in what the model sees',
}
ENGINE = ['Agentic RL', 'Self-distillation', 'Verifiable rewards', 'Test-time RL',
          'Evaluation · ageval', 'Steering · EasySteer']


def research_map(theme):
    t = THEMES[theme]
    W = 1200
    X0, BAND_R = 24, 952          # bands span X0..BAND_R
    SPX, SPW = 972, 204           # shared-engine spine
    HEAD = 256                    # header column inside each band
    GAP = 54
    LBL, WRK = 15.5, 14.5         # stage label / work font sizes
    CHIP_H1, CHIP_H2 = 58, 78     # chip heights for 1 / 2 works
    ROW_GAP, TAG_H = 16, 18

    # measure bands
    heights = []
    for letter, _, _, rows in BANDS:
        h = 28
        for ri, row in enumerate(rows):
            h += (TAG_H if letter in ROW_TAGS else 0) + max(CHIP_H2 if len(s[1]) > 1 else CHIP_H1 for s in row)
            h += ROW_GAP if ri < len(rows) - 1 else 0
        heights.append(h + 26)
    H = 24 + sum(heights) + GAP * (len(BANDS) - 1) + 86

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
         '<defs>',
         f'<marker id="ah" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M1,1 L9,5 L1,9 z" fill="{t["arrow"]}"/></marker>',
         f'<marker id="up" markerWidth="12" markerHeight="12" refX="6" refY="6" orient="auto"><path d="M1,2 L11,6 L1,10 z" fill="{t["arrow"]}"/></marker>',
         '</defs>',
         f'<rect width="{W}" height="{H}" rx="20" fill="{t["bg0"]}"/>']

    # spine behind everything
    sp_top, sp_bot = 24, 24 + sum(heights) + GAP * (len(BANDS) - 1)
    o.append(f'<rect x="{SPX}" y="{sp_top}" width="{SPW}" height="{sp_bot - sp_top}" rx="16" fill="{t["spine"]}" stroke="{t["panel_line"]}" stroke-width="1.5"/>')
    o.append(f'<text x="{SPX + SPW / 2}" y="{sp_top + 34}" text-anchor="middle" font-size="12.5" font-weight="700" letter-spacing="2.5" fill="{t["mute"]}">SHARED ENGINE</text>')
    o.append(f'<text x="{SPX + SPW / 2}" y="{sp_top + 54}" text-anchor="middle" font-size="12.5" fill="{t["mute"]}">across all four layers</text>')
    step = (sp_bot - sp_top - 120) / (len(ENGINE) - 1)
    for i, item in enumerate(ENGINE):
        y = sp_top + 100 + i * step
        o.append(f'<circle cx="{SPX + 26}" cy="{y - 5}" r="5" fill="{t["accent"]}"/>')
        o.append(f'<text x="{SPX + 40}" y="{y}" font-size="15.5" font-weight="600" fill="{t["ink"]}">{escape(item)}</text>')

    y = 24
    tops = []
    for (letter, name, verb, rows), bh in zip(BANDS, heights):
        base, light, darkc = LAYER[letter]
        tops.append((y, bh))
        fill = light if theme == 'light' else t['panel']
        o.append(f'<rect x="{X0}" y="{y}" width="{BAND_R - X0}" height="{bh}" rx="16" fill="{fill}" fill-opacity="{0.55 if theme == "light" else 1}" stroke="{base}" stroke-opacity="0.45" stroke-width="1.5"/>')
        # dashed tie to the spine
        o.append(f'<line x1="{BAND_R}" y1="{y + bh / 2}" x2="{SPX}" y2="{y + bh / 2}" stroke="{t["arrow"]}" stroke-width="1.2" stroke-dasharray="4 4"/>')
        # header
        cy = y + bh / 2
        o.append(f'<circle cx="{X0 + 46}" cy="{cy}" r="27" fill="{base}"/>')
        o.append(f'<text x="{X0 + 46}" y="{cy + 9}" text-anchor="middle" font-size="26" font-weight="800" fill="#FFFFFF">{letter}</text>')
        o.append(f'<text x="{X0 + 86}" y="{cy - 2}" font-size="22" font-weight="750" fill="{t["ink"]}">{name}</text>')
        o.append(f'<text x="{X0 + 86}" y="{cy + 21}" font-size="14.5" fill="{t["soft"]}">{verb}</text>')
        # stage rows
        ry = y + 26
        area_x, area_w = X0 + HEAD, BAND_R - X0 - HEAD - 18
        for ri, row in enumerate(rows):
            if letter in ROW_TAGS:
                o.append(f'<text x="{area_x}" y="{ry + 12}" font-size="11.5" font-weight="700" letter-spacing="1.6" fill="{base if theme == 'light' else BRIGHT[letter]}">{escape(ROW_TAGS[letter][ri])}</text>')
                ry += TAG_H
            ch = max(CHIP_H2 if len(s[1]) > 1 else CHIP_H1 for s in row)
            widths = [max(tw(s[0], LBL, True), *(tw(w_, WRK) for w_ in s[1])) + 30 for s in row]
            arrow = 30
            total = sum(widths) + arrow * (len(row) - 1)
            extra = (area_w - total) / len(row) if total < area_w else 0
            widths = [w_ + extra for w_ in widths]
            assert total <= area_w + 1, (name, total, area_w)
            x = area_x
            for si, (stage, works, *sys) in enumerate(row):
                w_ = widths[si]
                is_sys = bool(sys and sys[0])
                cfill = base if is_sys else t['chip']
                o.append(f'<rect x="{x}" y="{ry}" width="{w_}" height="{ch}" rx="11" fill="{cfill}" stroke="{base}" stroke-opacity="{1 if is_sys else 0.35}" stroke-width="1.2"/>')
                lab_col = '#FFFFFF' if is_sys else (base if theme == 'light' else BRIGHT[letter])
                o.append(f'<text x="{x + 15}" y="{ry + 23}" font-size="{LBL}" font-weight="700" fill="{lab_col}">{escape(stage)}</text>')
                for wi, work in enumerate(works):
                    col = '#FFFFFF' if is_sys else t['ink']
                    weight = '700' if is_sys else '500'
                    o.append(f'<text x="{x + 15}" y="{ry + 45 + wi * 20}" font-size="{WRK}" font-weight="{weight}" fill="{col}">{escape(work)}</text>')
                if si < len(row) - 1:
                    ax = x + w_ + 6
                    o.append(f'<line x1="{ax}" y1="{ry + ch / 2}" x2="{ax + arrow - 14}" y2="{ry + ch / 2}" stroke="{t["arrow"]}" stroke-width="1.6" marker-end="url(#ah)"/>')
                x += w_ + arrow
            ry += ch + ROW_GAP
        y += bh + GAP

    # upward hand-offs between layers
    order = [b[0] for b in BANDS]
    for i in range(len(BANDS) - 1):
        upper, lower = order[i], order[i + 1]
        label = LINKS.get((lower, upper))
        y_top = tops[i][0] + tops[i][1]
        y_bot = tops[i + 1][0]
        ax = X0 + 46
        o.append(f'<line x1="{ax}" y1="{y_bot - 4}" x2="{ax}" y2="{y_top + 10}" stroke="{t["arrow"]}" stroke-width="2" marker-end="url(#up)"/>')
        if label:
            o.append(f'<text x="{ax + 22}" y="{(y_top + y_bot) / 2 + 5}" font-size="14" font-style="italic" fill="{t["soft"]}">{escape(label)}</text>')

    # roots
    ry = sp_bot + 26
    o.append(f'<rect x="{X0}" y="{ry}" width="{W - 2 * X0}" height="40" rx="12" fill="{t["panel"]}" stroke="{t["panel_line"]}" stroke-width="1.2"/>')
    o.append(f'<text x="{X0 + 18}" y="{ry + 26}" font-size="12.5" font-weight="700" letter-spacing="2" fill="{t["mute"]}">ROOTS</text>')
    o.append(f'<text x="{X0 + 92}" y="{ry + 26}" font-size="15" fill="{t["soft"]}"><tspan font-weight="700" fill="{t["ink"]}">HuggingGPT</tspan> and <tspan font-weight="700" fill="{t["ink"]}">TaskBench</tspan>: LLMs as controllers of models and tools, where our agent line began</text>')
    o.append('</svg>')
    return '\n'.join(o)


for th in THEMES:
    open(f'{OUT}/banner-{th}.svg', 'w').write(banner(th))
    print(th, 'ok')
