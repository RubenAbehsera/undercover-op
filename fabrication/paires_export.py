"""Fige fabrication/paires.json depuis le graphe Neo4j (ADR 0001).

Le fichier produit est le contrat figé fabrication -> jeu : arcs, personnages
(avec notoriété calculée au moment de l'export), paires ordonnées selon le
classement structurel validé (requêtes 7.2/7.3). Le score lui-même n'y figure
pas — seul son ordre survit.

Garde-fous avant écriture :
- chaque lien du graphe doit être identique à sa seed (type, libellé,
  difficulté, arc) — un graphe pas régénéré fait échouer l'export ;
- difficulte dans l'enum, arcs et personnages référencés existent.

Usage: python paires_export.py   (le conteneur undercover-neo4j doit tourner)
"""

import csv
import io
import json
import os
import subprocess
import sys
from pathlib import Path

from neo4j_import import SEEDS, parse_paires

OUT = Path(__file__).resolve().parent / "paires.json"
MOT_DE_PASSE = os.environ.get("NEO4J_PASSWORD")
if not MOT_DE_PASSE:
    # docker compose lit fabrication/.env ; ce script Python, non — on y regarde.
    env = Path(__file__).resolve().parent / ".env"
    if env.exists():
        for ligne in env.read_text(encoding="utf-8").splitlines():
            if ligne.startswith("NEO4J_PASSWORD="):
                MOT_DE_PASSE = ligne.split("=", 1)[1].strip()
if not MOT_DE_PASSE:
    sys.exit("Mot de passe absent : définis NEO4J_PASSWORD (celui du compose, ex. dans fabrication/.env).")
CYPHER_SHELL = [
    "docker", "exec", "-i", "undercover-neo4j",
    "cypher-shell", "-u", "neo4j", "-p", MOT_DE_PASSE, "--format", "plain",
]


def requete(cypher: str) -> list[dict]:
    """Joue une requête en lisant la sortie plain de cypher-shell comme du CSV.

    La requête passe par stdin : en argument Windows, une requête multi-lignes
    arrive mutilée à cypher-shell.
    """
    r = subprocess.run(
        CYPHER_SHELL, input=cypher, capture_output=True, text=True,
        encoding="utf-8", check=True,
    )
    # skipinitialspace : l'en-tête plain de cypher-shell sépare par ", "
    # (« majorite, imposteur ») — sans lui les clés portent l'espace.
    lignes = csv.DictReader(io.StringIO(r.stdout), skipinitialspace=True)
    return [{k: v for k, v in l.items()} for l in lignes]


# Même formule que 7.3 : le score ne sert qu'à ordonner l'export.
SCORE = """
MATCH (a:Personnage)-[l:LIE_A]->(b:Personnage)
OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
MATCH (arc:Arc {id: l.arc}), (calibrage:Arc {id: 'dressrosa'})
WITH a, b, l, arc, calibrage, collect(DISTINCT g.nom) AS groupes
WITH a, b, l,
     CASE WHEN a.notoriete - b.notoriete > 10 THEN 25
          WHEN a.notoriete - b.notoriete > 4 THEN 15 ELSE 5 END
     + size(groupes) * 15
     + CASE WHEN arc.debut <= calibrage.debut THEN 10 ELSE 0 END AS score
RETURN a.id AS majorite, b.id AS imposteur, l.type AS type,
       l.libelle AS libelle, l.difficulte AS difficulte,
       l.arc AS arc_etablissement, score
ORDER BY score DESC, majorite
"""


def main() -> None:
    arcs = [r["id"] for r in requete("MATCH (x:Arc) RETURN x.id AS id ORDER BY x.debut;")]
    personnages = requete(
        "MATCH (p:Personnage) RETURN p.id AS id, p.nom AS nom, "
        "p.arc AS arc_premiere_apparition, p.notoriete AS notoriete "
        "ORDER BY p.chapitre, p.nom;"
    )
    # La sortie plain de cypher-shell est tout texte — la notoriété est un
    # nombre dans le contrat.
    for p in personnages:
        p["notoriete"] = int(p["notoriete"])
    connus = {p["id"] for p in personnages}
    liens = requete(SCORE)

    # Recoupement seeds <-> graphe : sens, champ à champ.
    seeds = {f"{p['majorite']}|{p['imposteur']}": p for p in parse_paires(SEEDS / "paires.candidates.yml")}
    graphe = {f"{l['majorite']}|{l['imposteur']}": l for l in liens}
    if set(seeds) != set(graphe):
        manq = set(seeds) - set(graphe)
        trop = set(graphe) - set(seeds)
        raise SystemExit(f"graphe et seeds divergent (manque: {manq}, en trop: {trop}) — régénérer l'import")

    paires = []
    for cle, l in graphe.items():
        s = seeds[cle]
        for champ in ("type", "libelle", "difficulte", "arc_etablissement"):
            if l[champ] != s[champ]:
                raise SystemExit(
                    f"{cle}: {champ} graphe={l[champ]!r} != seed={s[champ]!r} — régénérer l'import"
                )
        if l["difficulte"] not in ("facile", "intermediaire"):
            raise SystemExit(f"{cle}: difficulté hors enum : {l['difficulte']}")
        if l["arc_etablissement"] not in arcs:
            raise SystemExit(f"{cle}: arc inconnu : {l['arc_etablissement']}")
        if l["majorite"] not in connus or l["imposteur"] not in connus:
            raise SystemExit(f"{cle}: personnage inconnu")
        paires.append({
            "id": s["id"],
            "majorite": l["majorite"],
            "imposteur": l["imposteur"],
            "lien": {"type": l["type"], "libelle": l["libelle"]},
            "difficulte": l["difficulte"],
            "arc_etablissement": l["arc_etablissement"],
        })
    ids = [p["id"] for p in paires]
    if len(set(ids)) != len(ids):
        raise SystemExit("ids de paires en double")

    OUT.write_text(
        json.dumps(
            {"arcs": arcs, "personnages": personnages, "paires": paires},
            ensure_ascii=False, indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    scores = [int(l["score"]) for l in liens]
    print(f"{len(paires)} paires (scores {scores[0]}..{scores[-1]}), "
          f"{len(personnages)} personnages, {len(arcs)} arcs -> {OUT}")


if __name__ == "__main__":
    main()
