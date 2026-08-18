"""Revue LLM des paires candidates — des drapeaux, jamais des décisions.

Doctrine (docs/pipeline.md) : le LLM n'est jamais décideur. Il relit les
seeds en amont des requêtes, ancré sur les pages wiki en cache, et produit
des drapeaux dans seeds/paires.review.yml ; l'humain arbitre puis édite les
seeds. Rien d'automatique entre le graphe et l'export.

Appelle Z.ai (GLM) en direct, chat/completions style OpenAI, stdlib seule.
Sur une clé de coding plan la route est /api/coding/paas/v4 — l'API native
/api/paas/v4, elle, exige un solde payant (erreur 1113).

Usage : python llm_review.py [--out seeds/paires.review.yml] [--lot 8]
La revue se fait par lots de paires (défaut 8, réglable) : le corpus entier
d'un coup fait diverger le raisonnement du modèle et brûle le budget tokens.
Crédentials : ZAI_API_KEY, ou ANTHROPIC_AUTH_TOKEN (coding plan).
"""

import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from neo4j_import import parse_paires

try:
    import truststore

    truststore.inject_into_ssl()  # certificats de la machine (proxys TLS type Avast)
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent
SEEDS = ROOT / "seeds"
CACHE = ROOT / "cache"
MODELE = (
    os.environ.get("LLM_REVIEW_MODEL")
    or os.environ.get("ANTHROPIC_DEFAULT_OPUS_MODEL")
    or "glm-5.2"
)
BASE = os.environ.get("ZAI_BASE_URL") or "https://api.z.ai/api/coding/paas/v4"
CONTROLES = ("D", "S", "A", "L")

SYSTEME = """Tu relis les paires candidates d'un jeu d'ambiance One Piece (type
Undercover : chaque joueur reçoit un personnage, un membre de la minorité est
l'« imposteur » lié au personnage « majorité » d'un autre joueur). Ces paires
vivent dans un YAML de seeds et alimenteront un export figé consommé par le
jeu. Tu n'es qu'un relecteur : tu drapeautes, tu ne décides jamais — chaque
drapeau sera arbitré par un humain qui éditera les seeds.

Quatre contrôles, un code chacun :
- D (difficulté) : elle mesure ce que le GRAND PUBLIC connaît du duo, pas
  l'encodage du graphe. Un second emblématique (bras droit, duo iconique)
  reste « facile » même si le lien passe par un équipage partagé.
- S (sens) : majorite doit être le personnage le plus connu du grand public,
  imposteur l'autre. Signale les inversions probables.
- A (arc) : arc_etablissement sert l'anti-spoil — la paire n'est proposée
  qu'aux tables calibrées AU-DELÀ de cet arc. Signale les arcs trop tôt
  (risque de spoil) ou trop tard (sous-utilisation).
- L (libellé) : type parmi [rivalite, mentorat, parente, fraternite, equipage,
  alliance, faction, trahison, couple] + libellé. Signale les types impropres
  au lien réel.

Règles :
- Seulement des drapeaux actionnables ; proposition = changement précis
  (ex. « intermediaire -> facile »).
- Justification courte, ancrée sur l'extrait wiki fourni quand c'est possible.
- Une paire sans problème ne produit PAS de drapeau. Ne remplis pas pour
  remplir.
- Les remarques générales (couverture des arcs, doublons, calibrage) vont
  dans notes, pas en drapeaux.

Réponds uniquement par un objet JSON brut (aucune balise markdown, aucun
texte autour) : {"drapeaux": [{"paire": string, "controle": "D"|"S"|"A"|"L",
"proposition": string, "justification": string}], "notes": [string]}."""

BALISE = re.compile(r"<[^>]+>")
BRUIT = re.compile(r"(?is)<(script|style|sup|nav)[^>]*>.*?</\1>")


def extrait(page: Path, limite: int = 1200) -> str:
    """Début de texte visible d'une page wiki en cache (infobox + intro)."""
    texte = BALISE.sub(" ", BRUIT.sub(" ", page.read_text(encoding="utf-8")))
    return re.sub(r"\s+", " ", html.unescape(texte)).strip()[:limite]


def ligne_paire(p: dict) -> str:
    libelle = json.dumps(p["libelle"], ensure_ascii=False)
    return (
        f"- id: {p['id']} | majorite: {p['majorite']} | imposteur: {p['imposteur']}"
        f" | type: {p['type']} | difficulte: {p['difficulte']}"
        f" | arc: {p['arc_etablissement']} | libelle: {libelle}"
    )


def yaml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)  # JSON est du YAML valide


def appeler(contenu: str) -> dict:
    cle = os.environ.get("ZAI_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
    if not cle:
        sys.exit("Clé absente : définis ZAI_API_KEY (ou ANTHROPIC_AUTH_TOKEN).")
    charge = {
        "model": MODELE,
        "max_tokens": 16000,
        "thinking": {"type": "disabled"},
        "messages": [
            {"role": "system", "content": SYSTEME},
            {"role": "user", "content": contenu},
        ],
    }
    req = urllib.request.Request(
        BASE + "/chat/completions",
        data=json.dumps(charge).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + cle,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as rep:
            return json.load(rep)
    except urllib.error.HTTPError as e:
        sys.exit(f"Z.ai HTTP {e.code} : {e.read().decode('utf-8', 'replace')[:300]}")


def valider(rep: dict) -> tuple[list[dict], list[str]]:
    message = rep["choices"][0]["message"]
    texte = message.get("content") or ""
    m = re.search(r"\{.*\}", texte, re.S)
    if not m:
        sys.exit(f"Réponse non exploitable : {texte[:300]}")
    brut = json.loads(m.group(0))
    drapeaux = []
    for d in brut.get("drapeaux", []):
        if d.get("controle") not in CONTROLES:
            sys.exit(f"Contrôle inconnu : {json.dumps(d, ensure_ascii=False)}")
        for champ in ("paire", "proposition", "justification"):
            if not d.get(champ):
                sys.exit(f"Drapeau incomplet : {json.dumps(d, ensure_ascii=False)}")
        drapeaux.append(d)
    return drapeaux, [str(n) for n in brut.get("notes", [])]


def rendre(drapeaux: list[dict], notes: list[str]) -> str:
    lignes = [
        f"# Revue LLM — générée par fabrication/llm_review.py ({MODELE}).",
        "# Artefact régénérable ; l'état arbitré vit dans les seeds.",
        "# Doctrine (docs/pipeline.md) : le LLM n'est jamais décideur —",
        "# il drapeaute en amont des requêtes, l'humain arbitre et édite",
        "# les seeds. Jamais entre le graphe et l'export.",
        "# Contrôles : D difficulté · S sens majorite/imposteur · A arc",
        "#             d'établissement · L type/libellé.",
        "",
    ]
    if drapeaux:
        lignes.append("drapeaux:")
        for d in drapeaux:
            lignes += [
                f"  - paire: {yaml_str(d['paire'])}",
                f"    controle: {yaml_str(d['controle'])}",
                "    statut: \"à arbitrer\"",
                f"    proposition: {yaml_str(d['proposition'])}",
                f"    justification: {yaml_str(d['justification'])}",
            ]
    else:
        lignes.append("drapeaux: []")
    lignes.append("notes:")
    lignes += [f"  - {yaml_str(n)}" for n in notes] or ["  []"]
    return "\n".join(lignes) + "\n"


def contenu_pour(lot: list[dict]) -> str:
    personnages = sorted({p[k] for p in lot for k in ("majorite", "imposteur")})
    extraits = []
    for pid in personnages:
        page = CACHE / f"{pid}.html"
        texte = extrait(page) if page.exists() else "(page absente du cache)"
        extraits.append(f"### {pid}\n{texte}")
    return (
        f"Voici {len(lot)} paires candidates à relire dans ce lot, puis un"
        " extrait wiki (infobox/intro, tronqué) par personnage impliqué.\n\n"
        "## Paires\n" + "\n".join(ligne_paire(p) for p in lot)
        + "\n\n## Extraits wiki\n" + "\n\n".join(extraits)
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Revue LLM des paires candidates.")
    ap.add_argument("--out", type=Path, default=SEEDS / "paires.review.yml")
    ap.add_argument("--lot", type=int, default=8, help="taille des lots de paires")
    args = ap.parse_args()

    paires = parse_paires(SEEDS / "paires.candidates.yml")
    lots = [paires[i : i + args.lot] for i in range(0, len(paires), args.lot)]

    drapeaux, notes, usage = [], [], {"prompt_tokens": 0, "completion_tokens": 0}
    for n, lot in enumerate(lots, 1):
        print(f"lot {n}/{len(lots)} ({len(lot)} paires)...", flush=True)
        rep = appeler(contenu_pour(lot))
        d, note = valider(rep)
        drapeaux += d
        notes += note
        u = rep.get("usage", {})
        for k in usage:
            usage[k] += u.get(k, 0)

    args.out.write_text(rendre(drapeaux, notes), encoding="utf-8")
    print(
        f"{len(drapeaux)} drapeaux, {len(notes)} notes -> {args.out}"
        f" ({usage['prompt_tokens']} tokens en / {usage['completion_tokens']} hors)"
    )


if __name__ == "__main__":
    main()
