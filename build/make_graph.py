import json
import os
import random
import sys
import urllib.request
from pathlib import Path

LOGIN = "martinskb"
ROOT = Path(__file__).resolve().parent.parent
MONO = "ui-monospace, Menlo, Consolas, 'DejaVu Sans Mono', monospace"
LEVELS = {
    "NONE": "#1a0b10",
    "FIRST_QUARTILE": "#4a1a28",
    "SECOND_QUARTILE": "#6a1530",
    "THIRD_QUARTILE": "#8b1a3a",
    "FOURTH_QUARTILE": "#b3294f",
}
QUERY = (
    "query($login:String!){user(login:$login){contributionsCollection{contributionCalendar"
    "{totalContributions weeks{contributionDays{contributionLevel}}}}}}"
)


def fetch(token):
    body = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": "bearer " + token,
            "Content-Type": "application/json",
            "User-Agent": "profile-graph",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[d["contributionLevel"] for d in w["contributionDays"]] for w in cal["weeks"]]
    return cal["totalContributions"], weeks


def demo():
    rnd = random.Random(7)
    names = list(LEVELS)
    weeks = [[rnd.choice(names[:2] + names) for _ in range(7)] for _ in range(53)]
    return 200, weeks


def render(total, weeks):
    cell, gap, x0, y0 = 11, 2, 32, 70
    rects = []
    for wi, week in enumerate(weeks):
        for di, level in enumerate(week):
            x = x0 + wi * (cell + gap)
            y = y0 + di * (cell + gap)
            rects.append(
                f'<rect class="c" style="animation-delay:{wi * 0.04:.2f}s" x="{x}" y="{y}" '
                f'width="{cell}" height="{cell}" rx="2" fill="{LEVELS[level]}"/>'
            )
    legend = "".join(
        f'<rect x="{648 + i * 14}" y="176" width="11" height="11" rx="2" fill="{c}"/>'
        for i, c in enumerate(LEVELS.values())
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 210" width="100%" role="img" aria-label="Contribuições">
<style>
@keyframes pop{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes pulse{{0%,100%{{opacity:.7}}50%{{opacity:1}}}}
.c{{animation:pop .5s ease-out backwards}}
.pl{{animation:pulse 2.4s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{.c,.pl{{animation:none}}}}
</style>
<rect width="800" height="210" fill="#0a0607"/>
<rect x="0.5" y="0.5" width="799" height="209" fill="none" stroke="#3a1420"/>
<text class="pl" x="32" y="40" font-family="{MONO}" font-size="13" letter-spacing="3" fill="#b3294f">[ HISTÓRICO ]</text>
<text x="768" y="40" text-anchor="end" font-family="{MONO}" font-size="13" fill="#a8808c">{total} contribuições no último ano</text>
<line x1="32" y1="54" x2="768" y2="54" stroke="#4a1a28"/>
{"".join(rects)}
<text x="620" y="186" text-anchor="end" font-family="{MONO}" font-size="11" fill="#7c4a5a">menos</text>
{legend}
<text x="724" y="186" font-family="{MONO}" font-size="11" fill="#7c4a5a">mais</text>
</svg>
'''


if __name__ == "__main__":
    out = ROOT / "assets" / "graph.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    if "--demo" in sys.argv:
        total, weeks = demo()
    else:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
        try:
            total, weeks = fetch(token)
        except Exception as exc:
            print("grafico nao atualizado:", exc)
            sys.exit(0)
    out.write_text(render(total, weeks), encoding="utf-8")
    print(out)
