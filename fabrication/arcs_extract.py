"""Construit seeds/arcs.yml (arcs canoniques + bornes de chapitres).

Source: la page « Story Arcs » du wiki, mise en cache par curl/wiki_extract.
Les arcs sans plage de chapitres manga (anime-only) sont écartés d'office.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "cache" / "story_arcs.wikitext"
OUT = ROOT / "seeds" / "arcs.yml"

SAGA_RE = re.compile(r"^===\[\[([^\]|]+)(?:\|[^\]]*)?\]\]=", re.M)
ARC_RE = re.compile(r"^====\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", re.M)
CHAPTERS_RE = re.compile(r"\[\[:Category:[^\]]*Chapters\|Chapters\]\]:\s*[^\n(]*\(([0-9,\s\-]+)\)")


def slug(name: str) -> str:
    s = re.sub(r"[^\w\s-]", "", name.lower().strip())
    return re.sub(r"[\s_-]+", "_", s)


def main() -> None:
    w = SRC.read_text(encoding="utf-8")
    sagas = {m.start(): m.group(1) for m in SAGA_RE.finditer(w)}
    lines = ["# Généré par arcs_extract.py — arcs canoniques du manga, ordre chronologique.", ""]
    n = 0
    for m in ARC_RE.finditer(w):
        nom = re.sub(r"\s*Arc$", "", m.group(1))
        cm = CHAPTERS_RE.search(w, m.start(), m.start() + 4000)
        if not cm:
            continue
        nums = [int(x) for x in re.findall(r"\d+", cm.group(1))]
        pos_saga = max((p for p in sagas if p <= m.start()), default=None)
        saga = re.sub(r"\s*Saga$", "", sagas[pos_saga]) if pos_saga is not None else ""
        lines.append(f"- slug: {slug(nom)}")
        lines.append(f'  nom: "{nom}"')
        lines.append(f'  saga: "{saga}"')
        lines.append(f"  chapitres: [{nums[0]}, {nums[-1]}]")
        lines.append("")
        n += 1
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{n} arcs -> {OUT}")


if __name__ == "__main__":
    main()
