#!/usr/bin/env python3
"""Rebuild original Forklift Certified SVG artwork and PCM WAV sounds. Python stdlib only."""
from pathlib import Path
import json
import math
import random
import struct
import wave

ROOT = Path(__file__).resolve().parent
INK = '#293541'
CREAM = '#FAF2DF'
COLORS = {'purple': '#B5A0ED', 'mint': '#8DCBB5', 'coral': '#EE977D', 'yellow': '#F4BD48', 'blue': '#94B7F1', 'pink': '#F1AAD0'}
items = []


def svg(name, width, height, body, purpose, pivot=None):
    path = ROOT / (name + '.svg')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{body}</svg>\n')
    items.append({'path': str(path.relative_to(ROOT)), 'type': 'svg', 'width': width, 'height': height,
                  'pivot_normalized': pivot or [0.5, 0.5], 'purpose': purpose})


def rect(x, y, w, h, fill, radius=0, stroke=INK, sw=4):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def path(d, color=INK, width=4, fill='none'):
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def circle(x, y, r, fill, stroke=INK, sw=4):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


# Crates share dimensions and collider bounds; labels remain separate overlays.
for name, color in {'wood': '#DFB06B', **COLORS}.items():
    body = rect(4, 4, 200, 66, color, 3)
    body += path('M17 8V66 M191 8V66 M19 19H189 M19 55H189', '#746B65', 2)
    body += rect(68, 22, 72, 28, CREAM, 3, 'none', 0)
    body += path('M94 28V35 Q104 44 114 35V28 M104 39V45 M99 45H109', INK, 2)
    for x in (12, 196):
        for y in (12, 62):
            body += circle(x, y, 1.5, INK, 'none', 0)
    svg(f'sprites/crates/crate_{name}', 208, 74, body, 'Intact crate; collider rect (4,4,200,66).')
svg('sprites/crates/crate_crack_overlay', 208, 74, path('M133 5L123 19L135 31L122 44L132 56L123 69', INK, 3), 'Optional crack overlay; align with intact crate.')
for i, d in enumerate(['M4 4H72L55 25L69 39H4Z', 'M4 4L64 7L49 24L62 40L7 35Z', 'M4 9L63 4L71 29L44 24L29 40L8 30Z']):
    svg(f'sprites/debris/wood_chunk_{i+1}', 78, 46, path(d, INK, 3, '#DFB06B') + path('M13 17L44 18', '#A17A4D', 2), 'Cosmetic collapse debris; not gameplay physics.')
svg('sprites/props/pallet', 320, 48, rect(4, 4, 312, 22, '#B48757', 2) + ''.join(rect(x, 27, 27, 17, '#8D6546', 1) for x in (16, 102, 188, 274)) + path('M34 9V21 M110 9V21 M210 9V21 M284 9V21', '#785C42', 2), 'Stack base; top surface y=4.', [0.5, 4/48])

# Modular forklift, driver heads, and wheels for inexpensive animation.
svg('sprites/forklift/body', 176, 144, rect(8, 72, 108, 49, COLORS['yellow'], 9) + path('M28 70V12H92V70 M112 40H131V122H169', INK, 7) + rect(14, 79, 34, 17, '#FFE19B', 3, 'none', 0) + path('M75 58L65 76H90 M65 76V93', INK, 5), 'Forklift body facing right; wheel centers (32,124),(96,124); driver center (61,53).', [0.5, 124/144])
svg('sprites/forklift/wheel', 40, 40, circle(20, 20, 17, INK, INK, 2) + circle(20, 20, 8, '#77858A', 'none', 0) + path('M20 13V27 M13 20H27', INK, 3), 'Separate rotating wheel.')
for name, color in COLORS.items():
    for expression in ('neutral', 'panic', 'smug'):
        body = circle(28, 28, 23, color)
        if expression == 'neutral':
            body += path('M20 23V28 M36 23V28 M24 37H32', INK, 3)
        elif expression == 'panic':
            body += circle(19, 24, 3, INK, 'none', 0) + circle(37, 24, 3, INK, 'none', 0) + circle(28, 37, 5, INK, 'none', 0)
        else:
            body += path('M15 23L23 26 M33 26L41 23 M21 35Q28 43 37 33', INK, 3)
        svg(f'sprites/players/{name}_{expression}', 56, 56, body, 'Player avatar / forklift driver head; identity must also use a name or symbol.')

# Seamless environment tiles, fixed props, and decorative background.
svg('environment/wall_tile', 100, 80, rect(0, 0, 100, 80, '#EEE5D4', 0, 'none', 0) + path('M0 79H100 M99 0V80', '#DED4C2', 2), 'Seamless warehouse wall tile; repeat both axes.')
svg('environment/floor_tile', 100, 80, rect(0, 0, 100, 80, '#C4BDAE', 0, 'none', 0) + path('M0 79H100 M99 0V80', '#ACA99E', 2) + path('M18 27H35 M61 55H74', '#B6B0A2', 2), 'Seamless concrete tile.')
svg('environment/hazard_tile', 64, 24, rect(0, 0, 64, 24, COLORS['yellow'], 0, 'none', 0) + '<path d="M-24 24L0 0H16L-8 24Z M8 24L32 0H48L24 24Z M40 24L64 0H80L56 24Z" fill="#293541"/>', 'Repeat horizontally; clip to strip bounds.')
svg('environment/warehouse_backdrop', 1200, 600, rect(0, 0, 1200, 600, '#EEE5D4', 0, 'none', 0) + ''.join(path(f'M{x} 0V600', '#DED4C2', 8) for x in (100, 600, 1100)) + ''.join(path(f'M0 {y}H1200', '#DED4C2', 3) for y in (160, 320, 480)) + rect(755, 185, 330, 400, '#E0D7C5', 4, '#CBC5B6', 4) + ''.join(path(f'M765 {y}H1075', '#CBC5B6', 2) for y in range(210, 580, 28)), 'Optional low-contrast full-scene background; decorative only.')
svg('sprites/props/lamp', 160, 100, path('M80 0V40', INK, 5) + path('M50 42H110L142 78H18Z', INK, 4, '#77858A') + rect(30, 80, 100, 8, '#FFE19B', 3, 'none', 0), 'Hanging warehouse light.', [0.5, 0])
svg('sprites/props/cone', 64, 80, path('M25 5H39L53 65H11Z', INK, 4, '#EE977D') + path('M20 29H44 M16 47H48', CREAM, 8) + rect(4, 65, 56, 10, INK, 3), 'Decorative safety cone.')
svg('sprites/props/warning_sign', 96, 90, path('M48 5L90 80H6Z', INK, 4, COLORS['yellow']) + path('M48 29V51', INK, 7) + circle(48, 65, 4, INK, 'none', 0), 'Text-free caution sign.')

# UI backgrounds: use nine-slice margins from manifest companion theme.
for name, fill, outline in [('cream', CREAM, INK), ('dark', INK, INK), ('muted', '#E8DFCE', '#E8DFCE'), ('purple', COLORS['purple'], INK)]:
    svg(f'ui/panel_{name}', 96, 96, rect(3, 3, 90, 90, fill, 12, outline, 3), 'Nine-slice panel; 18px margins; no baked text.')
for state, fill, y in [('normal', INK, 3), ('hover', '#3D5160', 3), ('pressed', '#1B2731', 7), ('disabled', '#939A97', 3), ('focus', INK, 3)]:
    body = rect(5, 9, 182, 50, '#B8AE9B', 9, 'none', 0) + rect(5, y, 182, 48, fill, 9, 'none', 0)
    if state == 'focus':
        body += rect(2, 1, 188, 58, 'none', 12, COLORS['yellow'], 3)
    svg(f'ui/button_{state}', 192, 64, body, 'Nine-slice button; 18px margins. Add runtime label.')
svg('ui/keycap', 96, 64, rect(4, 9, 88, 50, '#B8AE9B', 8, 'none', 0) + rect(4, 3, 88, 49, CREAM, 8, INK, 3), 'Nine-slice input keycap; 14px margins; runtime binding label.')
svg('ui/turn_pointer', 32, 32, path('M5 4L27 16L5 28Z', INK, 2, COLORS['purple']), 'Current-player pointer.')
svg('ui/support_segment', 32, 12, rect(0, 1, 32, 10, '#50A586', 4, 'none', 0), 'Stretch over the valid landing interval; pair with outline for accessibility.')
svg('ui/drop_guide_tile', 8, 24, path('M4 2V12', '#7966A5', 2), 'Repeat vertically at crate edges during aiming.')
svg('ui/sweep_rail_tile', 32, 8, path('M0 4H32', '#AFB1A6', 4), 'Repeat horizontally behind sweeping crate.')
svg('ui/score_pip', 20, 20, circle(10, 10, 7, COLORS['coral'], INK, 2), 'Collapse penalty indicator; accompany with numeric score.')

icons = {
    'drop': 'M32 7V43 M19 30L32 43L45 30 M10 49V57H54V49',
    'arrow_right': 'M9 32H53 M38 17L53 32L38 47',
    'arrow_left': 'M55 32H11 M26 17L11 32L26 47',
    'check': 'M12 33L26 47L53 16',
    'close': 'M16 16L48 48 M48 16L16 48',
    'pause': 'M23 14V50 M41 14V50',
    'play': 'M22 12L51 32L22 52Z',
    'retry': 'M49 20A22 22 0 1 0 53 40 M49 7V22H34',
    'home': 'M8 29L32 9L56 29 M15 27V54H49V27 M27 54V37H37V54',
    'sound': 'M10 26H21L34 14V50L21 38H10Z M43 22Q55 32 43 42',
    'muted': 'M8 26H19L31 14V50L19 38H8Z M42 25L56 39 M56 25L42 39',
    'network': 'M10 23Q32 4 54 23 M18 33Q32 20 46 33 M26 43Q32 37 38 43 M32 53V54',
    'disconnected': 'M10 23Q32 4 54 23 M18 33Q32 20 46 33 M32 50V52 M9 8L55 56',
    'copy': 'M23 20H52V55H23Z M41 19V9H12V43H22',
    'lock': 'M19 29V21a13 13 0 0 1 26 0V29 M12 29H52V56H12Z M32 39V46',
    'clock': 'M32 13V32L44 39 M32 5A27 27 0 1 1 31.99 5',
    'trophy': 'M20 9H44V28Q44 43 32 43Q20 43 20 28Z M20 14H9V22Q9 32 21 32 M44 14H55V22Q55 32 43 32 M32 43V55 M22 55H42',
    'warning': 'M32 7L58 55H6Z M32 24V36 M32 45V46',
    'settings': 'M10 17H54 M10 32H54 M10 47H54 M23 10V24 M42 25V39 M28 40V54',
    'person': 'M32 8A10 10 0 1 1 31.99 8 M12 56V47Q12 33 32 33Q52 33 52 47V56',
}
for name, d in icons.items():
    for style, color in [('dark', INK), ('light', CREAM)]:
        svg(f'ui/icons/{name}_{style}', 64, 64, path(d, color, 4), 'Text-free UI icon; visible bounds inside 64px canvas.')

# Discrete frames, ordered for direct engine animation import.
for i in range(6):
    t = i / 5
    body = ''
    for j in range(7):
        angle = j * math.tau / 7
        radius = 10 + t * 34
        x, y = 64 + math.cos(angle)*radius, 76 + math.sin(angle)*radius*.45 - t*18
        r = (8 + t*9) * (1 - t*.65)
        body += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#B8AE9B" opacity="{(1-t*.9):.2f}"/>'
    svg(f'fx/dust/dust_{i:02}', 128, 128, body, 'Dust burst frame; 12fps, nonlooping, hide on finish.', [0.5, 0.625])
for i in range(4):
    body = ''
    for j in range(8):
        a = j*math.tau/8
        r1, r2 = 9+i*7, 22+i*8
        body += path(f'M{48+math.cos(a)*r1:.2f} {48+math.sin(a)*r1:.2f}L{48+math.cos(a)*r2:.2f} {48+math.sin(a)*r2:.2f}', COLORS['yellow'], 5-i)
    svg(f'fx/impact/impact_{i:02}', 96, 96, body, 'Impact frame; 16fps, nonlooping; hide on finish.')
svg('fx/shadow', 128, 32, '<ellipse cx="64" cy="16" rx="60" ry="12" fill="#293541" opacity=".18"/>', 'Stretchable soft-style flat ground shadow.')
for name, color in COLORS.items():
    svg(f'fx/confetti_{name}', 16, 20, rect(3, 3, 10, 14, color, 1, 'none', 0), 'Cosmetic result-screen particle.')

# Original mono PCM sounds: no samples or external synthesizers.
RATE = 44100

def sound(name, duration, kind, purpose, seed=1):
    rng = random.Random(seed)
    count = round(RATE * duration)
    data = []
    lp = 0.0
    for i in range(count):
        t = i / RATE
        u = t / duration
        attack = min(1, t/.008)
        fade = min(1, (duration-t)/.025)
        noise = rng.uniform(-1, 1)
        if kind in ('impact', 'collapse'):
            decay = math.exp(-t*(15 if kind == 'impact' else 4))
            lp = .7*lp + .3*noise
            value = (.65*lp + .4*math.sin(math.tau*(95*t-30*t*t))) * decay
            if kind == 'collapse':
                for onset in (.13, .29, .47, .66):
                    if t >= onset:
                        value += .16*noise*math.exp(-(t-onset)*28)
        elif kind == 'whoosh':
            lp = .9*lp + .1*noise
            value = lp * math.sin(math.pi*u)**2
        elif kind == 'motor':
            value = (.25*math.sin(math.tau*70*t) + .12*math.sin(math.tau*140*t) + .04*noise) * math.sin(math.pi*u)
        elif kind == 'tick':
            value = math.sin(math.tau*880*t)*math.exp(-t*45)
        elif kind == 'error':
            value = .45*math.sin(math.tau*155*t)*math.exp(-t*7) + .2*math.sin(math.tau*164*t)*math.exp(-t*7)
        elif kind in ('success', 'turn', 'win'):
            notes = {'success': [523.25, 659.25, 783.99], 'turn': [440, 659.25], 'win': [523.25, 659.25, 783.99, 1046.5]}[kind]
            step = duration/len(notes)
            n = min(len(notes)-1, int(t/step))
            local = t-n*step
            value = (.55*math.sin(math.tau*notes[n]*local) + .1*math.sin(math.tau*2*notes[n]*local))*min(1, local/.006)*math.exp(-local*9)
        else:
            value = math.sin(math.tau*(450*t+700*t*t))*math.exp(-t*35)
        data.append(value*attack*fade)
    peak = max(abs(v) for v in data) or 1
    gain = min(1.0, .72/peak)
    dest = ROOT / f'audio/sfx/{name}.wav'
    dest.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(dest), 'wb') as out:
        out.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
        out.writeframes(struct.pack('<'+'h'*count, *(round(v*gain*32767) for v in data)))
    items.append({'path': str(dest.relative_to(ROOT)), 'type': 'wav', 'duration_seconds': duration, 'sample_rate': RATE, 'channels': 1, 'loop': False, 'purpose': purpose})

for args in [
    ('ui_hover', .065, 'click', 'Optional hover feedback; play quietly.'),
    ('ui_click', .11, 'click', 'Button activation.'),
    ('ui_error', .24, 'error', 'Invalid action or join failure.'),
    ('player_join', .3, 'turn', 'Player joins lobby.'),
    ('player_leave', .25, 'error', 'Player leaves lobby.'),
    ('your_turn', .48, 'turn', 'Local player becomes active.'),
    ('countdown_tick', .10, 'tick', 'Final countdown second.'),
    ('crate_drop', .32, 'whoosh', 'Crate falling; optional pitch variation.'),
    ('crate_land', .32, 'impact', 'Successful placement contact.'),
    ('perfect_place', .5, 'success', 'Optional well-centered placement feedback; not a rule.'),
    ('wood_collapse', 1.05, 'collapse', 'Tower collapse.'),
    ('debris_hit', .18, 'impact', 'Sparse decorative debris impacts.'),
    ('timeout', .5, 'error', 'Turn timed out.'),
    ('shift_end', .7, 'success', 'End of round / shift.'),
    ('match_win', 1.4, 'win', 'Local player wins match.'),
    ('forklift_motor', .9, 'motor', 'Optional forklift movement one-shot; not seamless loop.'),
]:
    sound(*args)

palette = {'ink': INK, 'cream': CREAM, 'wall': '#EEE5D4', 'muted': '#E8DFCE', 'support': '#50A586', 'danger': '#EE977D', 'players': COLORS}
(ROOT/'palette.json').write_text(json.dumps(palette, indent=2)+'\n')
(ROOT/'ui/theme.json').write_text(json.dumps({'nine_slice_margins_px': {'panel_*': [18,18,18,18], 'button_*': [18,18,18,18], 'keycap': [14,14,14,14]}, 'reference_resolution': [1200,760], 'minimum_body_text_px': 18, 'font': 'Engine default initially; bundle a licensed font before release.', 'motion': {'dust_fps': 12, 'impact_fps': 16, 'reduce_motion': 'Disable shake, confetti, and large collapse camera motion.'}}, indent=2)+'\n')
(ROOT/'manifest.json').write_text(json.dumps({'title': 'Forklift Certified', 'version': 1, 'assets': items}, indent=2)+'\n')

# Contact sheet embeds generated artwork, so it remains a standalone SVG.
visuals = [a for a in items if a['type'] == 'svg']
cols, cw, ch = 6, 200, 148
height = 90 + math.ceil(len(visuals)/cols)*ch
body = rect(0, 0, 1200, height, '#E8DFCE', 0, 'none', 0)
body += '<text x="24" y="43" font-family="sans-serif" font-size="26" font-weight="bold" fill="#293541">FORKLIFT CERTIFIED / ASSET CONTACT SHEET</text>'
body += '<text x="24" y="69" font-family="sans-serif" font-size="14" fill="#293541">Original modular SVG artwork · dark-backed cells for visibility · see manifest for dimensions</text>'
for n, item in enumerate(visuals):
    x, y = n%cols*cw, 90+n//cols*ch
    body += rect(x+5, y+4, cw-10, 110, '#77858A', 6, 'none', 0)
    source = (ROOT/item['path']).read_text()
    inner = source[source.index('>')+1:source.rindex('</svg>')]
    scale = min(172/item['width'], 96/item['height'], 1.5)
    tx = x+100-item['width']*scale/2
    ty = y+59-item['height']*scale/2
    body += f'<g transform="translate({tx} {ty}) scale({scale})">{inner}</g>'
    label = Path(item['path']).stem
    body += f'<text x="{x+100}" y="{y+132}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#293541">{label}</text>'
(ROOT/'contact-sheet.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}">{body}</svg>\n')
print(f'Generated {len(visuals)} SVG assets, {len(items)-len(visuals)} WAV sounds, manifest, palette, theme, and contact sheet.')
