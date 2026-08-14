"""Construit seeds/personnages.yml (propre) depuis les sorties brutes.

- arc de première apparition : premier « Chapter N » du champ `first`,
  résolu par les bornes de arcs.yml
- groupes : équipages et factions dont le personnage est membre
  (catégories wiki croisées par slug — pas le champ affiliation en prose)
- fruit : dfname/dftype de l'infobox, s'ils existent

La notoriété n'est PAS ici : c'est le degré du nœud, calculé par le graphe.
"""

import json
import re
from pathlib import Path

from wiki_extract import slug

ROOT = Path(__file__).resolve().parent
SEEDS = ROOT / "seeds"


def parse_blocs(path: Path) -> dict:
    """Parse le sous-ensemble YAML émis par nos scripts (maps de scalaires + listes)."""
    data: dict = {}
    cur = None
    champ = None
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if not line.startswith((" ", "-")) and line.endswith(":"):
            cur = line[:-1]
            data[cur] = {}
        elif s.startswith("- "):
            data[cur].setdefault(champ, []).append(json.loads(s[2:]))
        else:
            m = re.match(r"^\s+([^:]+):(.*)$", line)
            if m and cur:
                champ = m.group(1).strip()
                v = m.group(2).strip()
                if v:
                    try:
                        data[cur][champ] = json.loads(v)
                    except ValueError:
                        data[cur][champ] = v
    return data


def parse_arcs(path: Path) -> list[tuple[str, int, int]]:
    arcs = []
    cur = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- slug: (.+)$", line)
        if m:
            cur = {"slug": m.group(1)}
            arcs.append(cur)
        elif cur:
            m = re.match(r"^  chapitres: \[(\d+), (\d+)\]$", line)
            if m:
                cur["debut"], cur["fin"] = int(m.group(1)), int(m.group(2))
    return [(a["slug"], a["debut"], a["fin"]) for a in arcs if "debut" in a]


def resoudre_arc(chapitre: int, arcs: list[tuple[str, int, int]]) -> str:
    for slug, debut, fin in arcs:
        if debut <= chapitre <= fin:
            return slug
    return arcs[-1][0]  # au-delà du dernier arc connu : arc en cours


def main() -> None:
    brut = parse_blocs(SEEDS / "personnages.brut.yml")
    arcs = parse_arcs(SEEDS / "arcs.yml")
    equipages = parse_blocs(SEEDS / "equipages.yml")
    factions = parse_blocs(SEEDS / "factions.yml")

    membres_equipages: dict[str, list[str]] = {}
    for crew, d in equipages.items():
        for titre in d.get("membres", []):
            membres_equipages.setdefault(slug(titre), []).append(crew)
    membres_factions: dict[str, list[str]] = {}
    for fac, d in factions.items():
        for titre in d.get("membres", []):
            membres_factions.setdefault(slug(titre), []).append(fac)

    lignes = [
        "# Généré par seeds_build.py — données propres pour le graphe.",
        "# arc_premiere_apparition résolu par chapitre ; groupes par catégories wiki.",
        "",
    ]
    sans_arc = []
    for ident, champs in brut.items():
        m = re.search(r"Chapter (\d+)", champs.get("first", ""))
        if not m:
            sans_arc.append(ident)
            continue
        chapitre = int(m.group(1))
        arc = resoudre_arc(chapitre, arcs)
        lignes.append(f"{ident}:")
        lignes.append(f'  nom: {json.dumps(champs.get("titre") or champs.get("page"), ensure_ascii=False)}')
        lignes.append(f"  chapitre_premiere_apparition: {chapitre}")
        lignes.append(f"  arc_premiere_apparition: {arc}")
        eq = sorted(membres_equipages.get(ident, []))
        fa = sorted(membres_factions.get(ident, []))
        lignes.append(f"  equipages: {json.dumps(eq, ensure_ascii=False)}")
        lignes.append(f"  factions: {json.dumps(fa, ensure_ascii=False)}")
        if champs.get("dfname"):
            lignes.append(f'  fruit: {{ nom: {json.dumps(champs["dfname"], ensure_ascii=False)}, type: {json.dumps(champs.get("dftype", ""), ensure_ascii=False)} }}')
        lignes.append("")

    (SEEDS / "personnages.yml").write_text("\n".join(lignes), encoding="utf-8")
    print(f"{len(brut) - len(sans_arc)} personnages enrichis -> seeds/personnages.yml")
    if sans_arc:
        print("sans chapitre trouvé:", ", ".join(sans_arc))


if __name__ == "__main__":
    main()
