"""Liste les membres des équipages connus (catégories du wiki) -> seeds/equipages.yml.

Parcourt chaque catégorie d'équipage et ses sous-catégories utiles
(les Vehicles/Weapons/Creations sont écartées). Croise avec seeds/pages.txt
et signale en sortie les membres absents du périmètre courant.
"""

import json
import re
import time
import urllib.parse
from pathlib import Path

from wiki_extract import fetch

API = "https://onepiece.fandom.com/api.php"
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "seeds" / "equipages.yml"
OUT_F = ROOT / "seeds" / "factions.yml"
PAGES = ROOT / "seeds" / "pages.txt"
PAUSE = 0.4
PROFONDEUR = 2

JUNK_SUBCAT = re.compile(r"(Vehicles|Weapons|Creations|Ships|Non-Canon)", re.I)

CREWS = {
    "straw_hat_pirates": "Straw Hat Pirates",
    "red_hair_pirates": "Red Hair Pirates",
    "roger_pirates": "Roger Pirates",
    "rocks_pirates": "Rocks Pirates",
    "whitebeard_pirates": "Whitebeard Pirates",
    "spade_pirates": "Spade Pirates",
    "heart_pirates": "Heart Pirates",
    "kid_pirates": "Kid Pirates",
    "kuja_pirates": "Kuja Pirates",
    "buggy_pirates": "Buggy Pirates",
    "cross_guild": "Cross Guild",
    "blackbeard_pirates": "Blackbeard Pirates",
    "big_mom_pirates": "Big Mom Pirates",
    "beasts_pirates": "Beasts Pirates",
    "sun_pirates": "Sun Pirates",
    "fire_tank_pirates": "Fire Tank Pirates",
}

FACTIONS = {
    "marines": "Marines",
    "sept_capitaines": "Seven Warlords of the Sea",
    "generation_terrible": "Worst Generation",
    "revolutionnaires": "Revolutionaries",
    "empereurs": "Four Emperors",
}


def walk(categorie: str, vus: set[str]) -> list[str]:
    if categorie in vus:
        return []
    vus.add(categorie)
    pages: list[str] = []
    cont = None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": categorie if categorie.startswith("Category:") else f"Category:{categorie}",
            "cmtype": "page|subcat",
            "cmlimit": 500,
            "format": "json",
        }
        if cont:
            params["cmcontinue"] = cont
        d = json.loads(fetch(f"{API}?{urllib.parse.urlencode(params)}"))
        if "error" in d:
            print(f"  !! {categorie}: {d['error'].get('info')}")
            return []
        for m in d["query"]["categorymembers"]:
            titre = m["title"]
            if titre.startswith("Category:"):
                if not JUNK_SUBCAT.search(titre):
                    pages += walk(titre, vus)
            else:
                pages.append(titre)
        cont = d.get("continue", {}).get("cmcontinue")
        time.sleep(PAUSE)
        if not cont:
            return pages


def main() -> None:
    perimetre = {
        l.strip()
        for l in PAGES.read_text(encoding="utf-8").splitlines()
        if l.strip() and not l.startswith("#")
    }
    lines = ["# Généré par equipages_extract.py — membres par équipage, sous-catégories comprises.", ""]
    for slug, cat in CREWS.items():
        mem = sorted(set(walk(f"Category:{cat}", set())))
        print(f"{cat}: {len(mem)} membres")
        lines.append(f"{slug}:")
        lines.append(f'  categorie: "{cat}"')
        lines.append("  membres:")
        for m in mem:
            lines.append(f"    - {json.dumps(m, ensure_ascii=False)}")
        lines.append("")
        hors = [m for m in mem if m not in perimetre]
        apercu = ", ".join(hors[:24]) + (f" … (+{len(hors) - 24})" if len(hors) > 24 else "")
        print(f"   hors périmètre ({len(hors)}): {apercu}")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"-> {OUT}")

    # Factions : mêmes catégories wiki, autre nature de groupe.
    lignes_f = ["# Généré par equipages_extract.py — membres par faction.", ""]
    for slug, cat in FACTIONS.items():
        mem = sorted(set(walk(f"Category:{cat}", set())))
        print(f"[faction] {cat}: {len(mem)} membres")
        lignes_f.append(f"{slug}:")
        lignes_f.append(f'  categorie: "{cat}"')
        lignes_f.append("  membres:")
        for m in mem:
            lignes_f.append(f"    - {json.dumps(m, ensure_ascii=False)}")
        lignes_f.append("")
    OUT_F.write_text("\n".join(lignes_f), encoding="utf-8")
    print(f"-> {OUT_F}")


if __name__ == "__main__":
    main()
