"""Gera os cartoes do README: equipamento (stack) e missoes (projetos)."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MONO = "ui-monospace, Menlo, Consolas, 'DejaVu Sans Mono', monospace"
WINE, CORAL = "#b3294f", "#e8704f"
STYLE = """<style>
@keyframes pulse{0%,100%{opacity:.7}50%{opacity:1}}
.pl{animation:pulse 2.4s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){.pl{animation:none}}
</style>"""

EQUIPAMENTO = [
    ("back-end", ["Node.js", "Express", "Python", "FastAPI", "Java"]),
    ("dados", ["SQL", "PostgreSQL", "MySQL", "SQLite", "Supabase", "Excel"]),
    ("front", ["React", "Vite", "PWA", "Flutter"]),
    ("infra", ["Linux", "Docker", "Git", "Vercel", "Cloudflare"]),
    ("testes", ["Vitest", "Supertest"]),
]

MISSOES = {
    "jacquemodas": ("Jacque Modas", "loja de roupas vendendo pelo WhatsApp:",
                    "bot oficial da Meta, Pix automático e estoque", "por tamanho e cor sem venda duplicada.",
                    ["Node.js", "PostgreSQL", "React"], "CLIENTE REAL"),
    "nexora": ("Nexora", "controle de vendas e estoque para o",
               "pequeno comerciante que ainda anota tudo", "no caderno, na planilha ou no WhatsApp.",
               ["Node.js", "MySQL", "React"], "ONLINE"),
    "lume": ("Lume", "app de estudos: cada tema vira um disco",
             "que gira enquanto você foca e evolui", "quanto mais você estuda.",
             ["FastAPI", "React", "PWA"], "ONLINE"),
    "amana": ("Amana", "agenda online para barbearias e salões:",
              "o cliente marca sozinho pelo link e o", "dono acompanha tudo pelo celular.",
              ["React", "Supabase", "PWA"], "EM ANDAMENTO"),
}


def frame(w, h, title, right=""):
    return (f'<rect width="{w}" height="{h}" fill="#0a0607"/>'
            f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" fill="none" stroke="#3a1420"/>'
            f'<text class="pl" x="24" y="34" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{WINE}">{title}</text>'
            f'<text x="{w - 24}" y="34" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="2" fill="#7c4a5a">{right}</text>'
            f'<line x1="24" y1="46" x2="{w - 24}" y2="46" stroke="#4a1a28"/>')


def chip(x, y, txt, cor="#cdb2ba", borda="#3a1420"):
    w = 14 + len(txt) * 7.3
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="22" rx="4" fill="#120a0d" stroke="{borda}"/>'
            f'<text x="{x + 7}" y="{y + 15}" font-family="{MONO}" font-size="12" fill="{cor}">{escape(txt)}</text>'), w


def equipamento():
    W, linha = 800, 34
    H = 64 + linha * len(EQUIPAMENTO)
    partes = [frame(W, H, "[ EQUIPAMENTO ]", "STACK")]
    for i, (grupo, itens) in enumerate(EQUIPAMENTO):
        y = 62 + i * linha
        partes.append(f'<text x="24" y="{y + 15}" font-family="{MONO}" font-size="12" fill="{CORAL}">{grupo}</text>')
        x = 120
        for it in itens:
            svg, w = chip(x, y, it)
            partes.append(svg)
            x += w + 8
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="stack">{STYLE}{"".join(partes)}</svg>\n'


def missao(nome, l1, l2, l3, tags, status):
    W, H = 390, 180
    partes = [frame(W, H, "[ MISSÃO ]", escape(status))]
    partes.append(f'<text x="24" y="80" font-family="{MONO}" font-size="22" fill="#f3e4e8">{escape(nome)}</text>')
    for k, t in enumerate((l1, l2, l3)):
        partes.append(f'<text x="24" y="{102 + k * 15}" font-family="{MONO}" font-size="11" fill="#a8808c">{escape(t)}</text>')
    x = 24
    for t in tags:
        svg, w = chip(x, 146, t, cor=CORAL)
        partes.append(svg)
        x += w + 6
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{escape(nome)}">{STYLE}{"".join(partes)}</svg>\n'


if __name__ == "__main__":
    out = ROOT / "assets"
    (out / "equipamento.svg").write_text(equipamento(), encoding="utf-8")
    for slug, dados in MISSOES.items():
        (out / f"missao-{slug}.svg").write_text(missao(*dados), encoding="utf-8")
    print("cartoes gerados")
