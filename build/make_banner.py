import base64
import math
import os
import sys
from datetime import date
from pathlib import Path

W, H = 800, 420
MONO = "ui-monospace, Menlo, Consolas, 'DejaVu Sans Mono', monospace"
WINE = "#b3294f"
CORAL = "#e8704f"
ROOT = Path(__file__).resolve().parent.parent

# slot -> (centro x, centro y, tamanho, rotacao em graus)
POSITIONS = {
    1: (500, 110, 70, -8),
    2: (640, 104, 56, 7),
    3: (712, 170, 64, -5),
    4: (565, 215, 60, 9),
    5: (700, 262, 70, -10),
    6: (470, 300, 54, 6),
    7: (610, 335, 62, -6),
    8: (395, 120, 58, 6),
    9: (365, 250, 54, -7),
}
CAPTIONS = {
    1: "Jujutsu Kaisen",
    2: "Resident Evil",
    3: "Final Fantasy 7",
    4: "Persona 5",
    5: "Pokémon",
    6: "Black Clover",
    7: "Solo Leveling",
    8: "Jurassic Park",
    9: "Star Wars",
}
# cor principal de cada franquia (se for vermelho, entra a segunda cor)
COLORS = {
    1: "#4d7cff",
    2: "#3fbf6f",
    3: "#2ee6c8",
    4: "#f2f2f2",
    5: "#f7d02c",
    6: "#9aa0ab",
    7: "#9b6bff",
    8: "#f28c28",
    9: "#8fd3ff",
}


def age_from(birth, today=None):
    today = today or date.today()
    years = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        years -= 1
    return years


def level_label():
    raw = os.environ.get("BIRTHDATE", "").strip()
    if not raw:
        return "??"
    try:
        return str(age_from(date.fromisoformat(raw)))
    except ValueError:
        return "??"


def spiral():
    pts = []
    for i in range(0, 90):
        t = i / 89
        a = t * 3.2 * math.pi * 2
        r = 4 + t * 24
        pts.append(f"{r * math.cos(a):.1f},{r * math.sin(a):.1f}")
    return "M" + " L".join(pts)


GLYPHS = {
    1: f'<path d="{spiral()}"/>',
    2: '<circle cx="-14" cy="-14" r="10"/><path d="M-7 -7 L22 22 M12 12 L18 6 M19 19 L25 13"/>',
    3: '<polygon points="0,-26 19,-8 0,26 -19,-8"/><path d="M-19 -8 L19 -8 M0 -26 L-7 -8 L0 26 M0 -26 L7 -8 L0 26"/>',
    4: '<rect x="-26" y="-18" width="52" height="36" rx="3"/><path transform="translate(0 1) scale(0.55)" d="M0 20 C-32 -2 -16 -26 0 -9 C16 -26 32 -2 0 20Z"/>',
    5: '<path d="M7 -27 L-15 4 L-2 4 L-7 27 L15 -6 L2 -6 Z"/>',
    6: '<path d="M0 -14 L0 18 M0 -14 C-10 -20 -22 -18 -29 -14 L-29 16 C-22 12 -10 12 0 18 C10 12 22 12 29 16 L29 -14 C22 -18 10 -20 0 -14Z"/>',
    7: '<path d="M-20 4 L0 -16 L20 4 M-20 22 L0 2 L20 22"/>',
    8: '<ellipse cx="0" cy="14" rx="12" ry="10"/><ellipse cx="-17" cy="-4" rx="5" ry="10"/><ellipse cx="0" cy="-12" rx="5" ry="11"/><ellipse cx="17" cy="-4" rx="5" ry="10"/>',
    9: '<circle r="13"/><ellipse rx="28" ry="8" transform="rotate(-20)"/><circle cx="-24" cy="-20" r="1.6" fill="currentColor"/><circle cx="22" cy="-22" r="1.6" fill="currentColor"/><circle cx="24" cy="20" r="1.6" fill="currentColor"/>',
}

STYLE = """<style>
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes twinkle{0%,100%{opacity:.2}50%{opacity:1}}
@keyframes pulse{0%,100%{opacity:.7}50%{opacity:1}}
@keyframes type{from{width:0}to{width:260px}}
.f{animation:float 4s ease-in-out infinite}
.b{animation:blink 1s steps(1) infinite}
.tw{animation:twinkle 3s ease-in-out infinite}
.pl{animation:pulse 2.4s ease-in-out infinite}
.t1{animation:type 1.1s steps(20) 0.3s 1 backwards}
.t2{animation:type 1.1s steps(22) 1.5s 1 backwards}
.t3{animation:type 1.1s steps(21) 2.7s 1 backwards}
@media (prefers-reduced-motion:reduce){.f,.b,.tw,.pl,.t1,.t2,.t3{animation:none}}
</style>"""


def icon_data_uri(path):
    data = Path(path).read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode()


def slot_markup(slot, icons, captions=True):
    cx, cy, size, rot = POSITIONS[slot]
    if slot in icons:
        half = size / 2
        body = (
            f'<g transform="rotate({rot} {cx} {cy})"><image x="{cx - half}" y="{cy - half}" '
            f'width="{size}" height="{size}" preserveAspectRatio="xMidYMid meet" '
            f'href="{icon_data_uri(icons[slot])}"/></g>'
        )
    else:
        scale = size / 64
        base = COLORS[slot]
        common = 'stroke-linecap="round" stroke-linejoin="round" fill="none"'
        body = (
            f'<g transform="translate({cx} {cy}) rotate({rot}) scale({scale:.3f})">'
            f'<g stroke="{base}" color="{base}" stroke-width="2.4" {common}>{GLYPHS[slot]}</g>'
            f'<g stroke="{WINE}" color="{WINE}" stroke-width="1" opacity="0.55" {common}>{GLYPHS[slot]}</g>'
            f'</g>'
        )
    cap = ""
    if captions:
        cap = (
            f'<text x="{cx}" y="{cy + size / 2 + 16}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="11" fill="#7c4a5a">{CAPTIONS[slot]}</text>'
        )
    dur = 3.4 + (slot % 4) * 0.6
    delay = -(slot * 0.7)
    return f'<g class="f" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s">{body}{cap}</g>'


def make_banner(icons=None, captions=True, level="??"):
    icons = icons or {}
    spots = [(430, 60), (560, 150), (780, 60), (440, 200), (770, 330), (540, 390), (690, 190), (330, 170)]
    marks = "".join(
        f'<text class="tw" style="animation-delay:{-i * 0.9:.1f}s" x="{x}" y="{y}" '
        f'font-family="{MONO}" font-size="14" fill="#5a2132">+</text>'
        for i, (x, y) in enumerate(spots)
    )
    slots = "".join(slot_markup(s, icons, captions) for s in sorted(POSITIONS))
    quote = (
        "Não sei como vou me sentir quando estiver morto,",
        "mas não quero me arrepender da maneira como vivi.",
    )
    clips = "".join(
        f'<clipPath id="c{i}"><rect class="t{i}" x="32" y="{y - 20}" width="260" height="28"/></clipPath>'
        for i, y in ((1, 188), (2, 218), (3, 248))
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="kaio">
{STYLE}
<defs>{clips}</defs>
<rect width="{W}" height="{H}" fill="#0a0607"/>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="#3a1420"/>
<text class="pl" x="32" y="44" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{WINE}">[ SAVE ROOM ]</text>
<text class="pl" x="{W - 32}" y="44" text-anchor="end" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{WINE}">LV. {level}</text>
<line x1="32" y1="58" x2="{W - 32}" y2="58" stroke="#4a1a28"/>
{marks}
<text x="32" y="140" font-family="{MONO}" font-size="46" fill="#f3e4e8">kaio</text>
<g font-family="{MONO}" font-size="16" fill="#cdb2ba">
<text clip-path="url(#c1)" x="32" y="188"><tspan fill="{WINE}">&gt;</tspan> construindo coisas</text>
<text clip-path="url(#c2)" x="32" y="218"><tspan fill="{WINE}">&gt;</tspan> aprendendo no caminho</text>
<text clip-path="url(#c3)" x="32" y="248"><tspan fill="{WINE}">&gt;</tspan> salvando progresso<tspan class="b" fill="{CORAL}">_</tspan></text>
</g>
{slots}
<g font-family="{MONO}" font-size="14" font-style="italic" fill="#a8808c">
<text x="32" y="362">{quote[0]}</text>
<text x="32" y="386">{quote[1]}</text>
</g>
</svg>
'''


def discover_icons():
    found = {}
    for slot in POSITIONS:
        path = ROOT / "assets" / "icons" / f"{slot}.png"
        if path.exists():
            found[slot] = path
    return found


if __name__ == "__main__":
    icons = discover_icons()
    for arg in sys.argv[1:]:
        slot, path = arg.split("=", 1)
        icons[int(slot)] = path
    out = ROOT / "assets" / "banner.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(make_banner(icons, level=level_label()), encoding="utf-8")
    print(out)
