"""Extrait les portraits des personnages du cache wiki, pour le front.

Usage:
    python portraits_extract.py

Entrée: fabrication/paires.json (les personnages réellement tirables) et le
cache HTML de wiki_extract. Sortie: front/public/personnages/<id>.webp — le
second artefact figé fabrication → jeu, servi en statique, jamais relu par le
serveur.

L'onglet d'infobox retenu est l'anime d'avant l'ellipse quand il existe : une
apparence d'après trahirait déjà la suite à une table calibrée tôt.
"""

import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
PAIRES = ROOT / "paires.json"
SORTIE = ROOT.parent / "front" / "public" / "personnages"
LARGEUR = 256
PAUSE = 0.3  # politesse entre requêtes

COLLECTION_RE = re.compile(r'<div class="pi-image-collection.*?\n\t</div>', re.S)
ONGLET_RE = re.compile(r'wds-tabs__tab-label">\s*(.*?)\s*</span>', re.S)
FIGURE_RE = re.compile(r'<figure class="pi-item pi-image".*?</figure>', re.S)
SRC_RE = re.compile(r'<img[^>]+\bsrc="([^"]+)"')
ECHELLE_RE = re.compile(r"/scale-to-width-down/\d+")
PREFERENCES = ("anime pre-timeskip", "anime")


def portrait_url(id_personnage: str) -> str:
    """L'URL de l'onglet d'infobox préféré, ramenée à la largeur voulue."""
    html = (CACHE / f"{id_personnage}.html").read_text(encoding="utf-8")
    collection = COLLECTION_RE.search(html)
    portion = collection.group(0) if collection else html
    figures = FIGURE_RE.findall(portion)
    if not figures:
        raise LookupError(f"pas d'image d'infobox pour {id_personnage}")
    onglets = [libelle.lower() for libelle in ONGLET_RE.findall(portion)]
    source = SRC_RE.search(figures[_rang(onglets, len(figures))])
    if not source:
        raise LookupError(f"figure sans image pour {id_personnage}")
    url = source.group(1).split("?")[0]
    if ECHELLE_RE.search(url):
        return ECHELLE_RE.sub(f"/scale-to-width-down/{LARGEUR}", url)
    return f"{url}/scale-to-width-down/{LARGEUR}"


def _rang(onglets: list[str], figures: int) -> int:
    """L'onglet préféré, à défaut le premier — les deux listes vont de pair."""
    if len(onglets) != figures:
        return 0
    for voulu in PREFERENCES:
        if voulu in onglets:
            return onglets.index(voulu)
    return 0


def telecharger(url: str) -> bytes:
    entetes = {
        "User-Agent": "undercover-op-fabrication/0.1",
        # Le CDN convertit à la volée : une seule extension pour tous.
        "Accept": "image/webp",
    }
    req = urllib.request.Request(url, headers=entetes)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read()
    except urllib.error.URLError:
        # OpenSSL (Python) rejette la chaîne du proxy local ; curl l'accepte.
        return subprocess.run(
            ["curl", "-s", "--max-time", "30", "-H", "Accept: image/webp", url],
            capture_output=True,
            check=True,
        ).stdout


def personnages() -> list[str]:
    contrat = json.loads(PAIRES.read_text(encoding="utf-8"))
    tirables = {paire["majorite"] for paire in contrat["paires"]}
    tirables |= {paire["imposteur"] for paire in contrat["paires"]}
    return sorted(tirables)


def main() -> int:
    SORTIE.mkdir(parents=True, exist_ok=True)
    manquants = []
    for id_personnage in personnages():
        fichier = SORTIE / f"{id_personnage}.webp"
        if fichier.exists():
            continue
        try:
            image = telecharger(portrait_url(id_personnage))
        except (LookupError, OSError, subprocess.CalledProcessError) as err:
            manquants.append(f"{id_personnage} : {err}")
            continue
        if not (image[:4] == b"RIFF" and image[8:12] == b"WEBP"):
            manquants.append(f"{id_personnage} : reponse qui n'est pas un webp")
            continue
        fichier.write_bytes(image)
        print(f"{id_personnage} - {len(image) // 1024} Ko")
        time.sleep(PAUSE)
    for ligne in manquants:
        print(f"MANQUANT {ligne}", file=sys.stderr)
    return 1 if manquants else 0


if __name__ == "__main__":
    raise SystemExit(main())
