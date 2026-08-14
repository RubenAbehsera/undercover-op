"""Génère neo4j/import.cypher depuis les seeds — nœuds et relations du graphe.

Pourquoi un générateur plutôt que du Cypher écrit à la main : les seeds sont
des données (YAML re-régénéré depuis le wiki), le graphe doit pouvoir être
reconstruit de zéro à tout moment. Le .cypher produit est un artefact jetable.

Le modèle cible (voir neo4j/guide.md) :

    (:Personnage {id, nom, chapitre, arc})
    (:Personnage)-[:MEMBRE_DE]->(:Equipage | :Faction)
    (:Personnage)-[:MANGE]->(:Fruit {nom, type})
    (:Personnage)-[:PREMIERE_APPARITION]->(:Arc {id, debut, fin})
    (:Personnage)-[:LIE_A {type, libelle, difficulte, arc}]->(:Personnage)

Deux points Cypher à comprendre avant de modifier ce fichier :

1. MERGE = « trouve-ou-crée » sur TOUT le motif passé. Rejouer le script ne
   duplique donc rien (CREATE, lui, dupliquerait). C'est ce qui rend l'import
   idempotent.
2. Piège classique de MERGE : si le motif contient des variables non encore
   liées (ex. MERGE (a)-[:REL]->(b) avec a et b libres), et qu'il n'y a pas
   de correspondance, Neo4j crée a, b ET la relation — des doublons. D'où le
   patron systématique ci-dessous : MATCH des deux extrémités d'abord
   (déjà créées, identifiées par leur clé unique), puis MERGE de la relation
   entre variables liées.

Usage: python neo4j_import.py   puis   cypher-shell < neo4j/import.cypher
"""

import json
import re
from pathlib import Path

from seeds_build import parse_arcs, parse_blocs

ROOT = Path(__file__).resolve().parent
SEEDS = ROOT / "seeds"
OUT = ROOT / "neo4j" / "import.cypher"


def cypher_str(s: str) -> str:
    # Échappement minimal : backslash puis guillemet. (Neo4j accepte aussi
    # l'unicode brut, pas besoin d'ascii-ifier.)
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_paires(path: Path) -> list[dict]:
    """Parse le sous-ensemble YAML de paires.candidates.yml (pas de PyYAML ici)."""
    paires = []
    cur = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- id: "):
            cur = {"id": line[6:].strip()}
            paires.append(cur)
        elif cur:
            m = re.match(r"^  (\w+): (.+)$", line)
            if m:
                k, v = m.group(1), m.group(2).strip()
                if k == "lien":
                    # ligne de la forme: lien: { type: rivalite, libelle: "..." }
                    lm = re.match(r"\{ type: (\w+), libelle: (.+) \}$", v)
                    cur["type"] = lm.group(1)
                    cur["libelle"] = json.loads(lm.group(2))
                else:
                    cur[k] = v
    return paires


def main() -> None:
    pers = parse_blocs(SEEDS / "personnages.yml")
    equipages = parse_blocs(SEEDS / "equipages.yml")
    factions = parse_blocs(SEEDS / "factions.yml")
    arcs = parse_arcs(SEEDS / "arcs.yml")
    paires = parse_paires(SEEDS / "paires.candidates.yml")

    c = ["// Généré par neo4j_import.py — ne pas éditer à la main.", ""]

    # Réinitialisation complète. DETACH DELETE supprime d'abord les relations
    # (un DELETE nu refuse un nœud encore relié — sécurité du modèle graphe).
    c.append("MATCH (n) DETACH DELETE n;")

    # Arcs d'abord : les personnages y font référence via PREMIERE_APPARITION.
    # La clé d'identité est l'id (slug) ; debut/fin servent aux comparaisons
    # de calibrage (cf. queries.cypher 5.3).
    c.append("")
    for a_slug, debut, fin in arcs:
        c.append(
            f"MERGE (:Arc {{id: {cypher_str(a_slug)}, debut: {debut}, fin: {fin}}});"
        )

    # Groupes : MERGE sur l'id (slug) comme clé unique, nom lisible en propriété.
    c.append("")
    for e, d in equipages.items():
        cat = d.get("categorie", e)
        c.append(f"MERGE (:Equipage {{id: {cypher_str(e)}, nom: {cypher_str(cat)}}});")
    for f, d in factions.items():
        cat = d.get("categorie", f)
        c.append(f"MERGE (:Faction {{id: {cypher_str(f)}, nom: {cypher_str(cat)}}});")

    # Personnages + relations sortantes. Chaque ligne = une instruction
    # terminée par ';' : cypher-shell lit le fichier instruction par
    # instruction. Une relation EST son propre identifiant — pas de colonne
    # id, MERGE sur le motif complet suffit.
    c.append("")
    for ident, d in pers.items():
        fruit = d.get("fruit", "")
        props = [
            f"id: {cypher_str(ident)}",
            f"nom: {cypher_str(d['nom'])}",
            f"chapitre: {d['chapitre_premiere_apparition']}",
            f"arc: {cypher_str(d['arc_premiere_apparition'])}",
        ]
        # Nœud + arc de première apparition : un seul MERGE en chaîne suffit,
        # les deux motifs partagent la variable p.
        c.append(f"MERGE (p:Personnage {{{', '.join(props)}}})")
        c.append(
            f"MERGE (a:Arc {{id: {cypher_str(d['arc_premiere_apparition'])}}}) "
            f"MERGE (p)-[:PREMIERE_APPARITION]->(a);"
        )
        # Patron MATCH-then-MERGE : les extrémités existent déjà.
        for e in d.get("equipages", []):
            c.append(
                f"MATCH (p:Personnage {{id: {cypher_str(ident)}}}) "
                f"MATCH (g:Equipage {{id: {cypher_str(e)}}}) "
                f"MERGE (p)-[:MEMBRE_DE]->(g);"
            )
        for f in d.get("factions", []):
            c.append(
                f"MATCH (p:Personnage {{id: {cypher_str(ident)}}}) "
                f"MATCH (g:Faction {{id: {cypher_str(f)}}}) "
                f"MERGE (p)-[:MEMBRE_DE]->(g);"
            )
        # Fruits : MERGE par (nom, type). Cas curieux visible dans le graphe :
        # la Mera Mera no Mi est mangée par Ace ET Sabo (succession canonique)
        # — le MERGE par nom fusionne les deux, exactement ce qu'on veut.
        if fruit:
            m = re.match(r"\{ nom: (.+), type: (.+) \}$", fruit)
            if m:
                nom_f, type_f = json.loads(m.group(1)), json.loads(m.group(2))
                c.append(
                    f"MERGE (f:Fruit {{nom: {cypher_str(nom_f)}, type: {cypher_str(type_f)}}});"
                )
                c.append(
                    f"MATCH (p:Personnage {{id: {cypher_str(ident)}}}) "
                    f"MATCH (f:Fruit {{nom: {cypher_str(nom_f)}}}) "
                    f"MERGE (p)-[:MANGE]->(f);"
                )

    # LIE_A : la couche humaine, direction majorite -> imposteur. Les
    # propriétés portées par la relation (type, libelle, difficulte, arc)
    # sont ce que le serveur de jeu lira dans paires.json à terme.
    c.append("")
    for p in paires:
        c.append(
            f"MATCH (a:Personnage {{id: {cypher_str(p['majorite'])}}}), "
            f"(b:Personnage {{id: {cypher_str(p['imposteur'])}}}) "
            f"MERGE (a)-[:LIE_A {{type: {cypher_str(p['type'])}, "
            f"libelle: {cypher_str(p['libelle'])}, "
            f"difficulte: {cypher_str(p['difficulte'])}, "
            f"arc: {cypher_str(p['arc_etablissement'])}}}]->(b);"
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(c) + "\n", encoding="utf-8")
    print(f"{len(pers)} personnages, {len(arcs)} arcs, {len(paires)} liens -> {OUT}")


if __name__ == "__main__":
    main()
