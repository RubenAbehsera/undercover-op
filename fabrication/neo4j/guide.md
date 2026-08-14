# Parcours Neo4j — apprendre sur notre graphe

Objectif : que tu écrives toi-même les requêtes de fabrication (validation des
paires, proposeur) puis, à terme, le réglage des poids. Le graphe est **jetable** :
tout se régénère depuis les seeds. Casse-le sans peur.

## Setup

    cd fabrication
    docker compose up -d        # démarre Neo4j (premier lancement : ~1 min)
    # Browser : http://localhost:7474 — neo4j / mot-de-passe-supprime

Tout casser et recommencer :

    python neo4j_import.py      # régénère neo4j/import.cypher depuis les seeds
    docker exec -i undercover-neo4j cypher-shell -u neo4j -p mot-de-passe-supprime \
      --format plain < neo4j/import.cypher

## Le modèle en une minute

Un graphe de propriétés n'a que trois briques :

- **Nœud** : une entité, portant un ou plusieurs _labels_ (`:Personnage`, `:Equipage`).
- **Relation** : une flèche _typée et orientée_ entre deux nœuds (`-[:MEMBRE_DE]->`).
  Une vraie arête physique, pas une foreign key : la parcourir coûte O(1),
  là où un JOIN SQL se paie à chaque saut.
- **Propriété** : clé/valeur, sur les nœuds (`nom`, `chapitre`) ET les relations
  (`LIE_A.type`, `LIE_A.arc`).

Notre schéma :

    (:Personnage)-[:MEMBRE_DE]->(:Equipage | :Faction)
    (:Personnage)-[:MANGE]->(:Fruit)
    (:Personnage)-[:PREMIERE_APPARITION]->(:Arc {debut, fin})
    (:Personnage)-[:LIE_A {type, libelle, difficulte, arc}]->(:Personnage)

`LIE_A` est la couche humaine (les 32 paires candidates) ; tout le reste vient
des catégories wiki. Le rôle de chacun : `docs/pipeline.md`.

## La doc, dans l'ordre

1. **Concepts** — Getting Started, « property graph structural concepts » :
   https://neo4j.com/docs/getting-started/
2. **Cypher Manual** — ta référence permanente, à lire au fil des niveaux
   (sections : Patterns, MATCH, WHERE, RETURN, MERGE, Aggregation,
   variable-length patterns, shortestPath) :
   https://neo4j.com/docs/cypher-manual/current/
3. **GraphAcademy** — gratuit, ~2 h, le cours « Cypher Fundamentals » :
   https://graphacademy.neo4j.com/

Règle d'or avant chaque exo : formule la phrase en français — « les personnages
qui… » se traduit quasi mot à mot en motif. La requête EST la phrase.

## Les niveaux

Chaque niveau : lis la doc → fais les exos dans le Browser, sans copier-coller →
compare avec le corrigé commenté dans `queries.cypher` (même numéro).

### Niveau 1 — Lire (20 min)

Doc : Cypher Manual → MATCH / WHERE / RETURN.

1. Les 10 premiers personnages, nom seul.MATCH (n:Personnage) RETURN n.nom LIMIT 10;
2. La fiche complète de Nami. -> MATCH (n:Personnage {nom:'Nami'}) RETURN n LIMIT 25;
3. Les personnages apparus avant le chapitre 50, triés par chapitre. -> MATCH (n:Personnage) WHERE n.chapitre < 50 RETURN n ORDER BY n.chapitre;
4. Les fruits dont le type contient « Zoan ». -> MATCH (n:Fruit) WHERE n.type CONTAINS "Zoan" return n

### Niveau 2 — Motifs de relations (30 min)

Doc : Cypher Manual → Patterns (la syntaxe ASCII-art).

1. Les groupes de Jinbe, avec leur label (Equipage ou Faction ?). -> MATCH (p:Personnage {nom:'Jinbe'})-[:MEMBRE_DE]->(a:Equipage | Faction)
   RETURN a as appartenance
2. Les Chapeaux de Paille triés par ordre d'arrivée dans le manga. -> MATCH (p:Personnage)-[:MEMBRE_DE]->(a:Equipage {id : 'straw_hat_pirates'})
   RETURN p as perssonage, a as appartenance ORDER by p.chapitre
3. Qui mange quel fruit chez les Chapeaux de Paille. ->MATCH (p:Personnage)-[:MEMBRE_DE]->(a:Equipage {id : 'straw_hat_pirates'})
   WITH p as perssonages
   ORDER BY perssonages.chapitre
   MATCH (perssonages)-[:MANGE]->(f:Fruit)
   RETURN perssonages.nom as Personnage, f as Fruit

4. Les membres à la fois Génération Terrible et Empereurs. -> MATCH (p:Personnage)-[:MEMBRE_DE]->(e:Equipage {id: 'straw_hat_pirates'})
   MATCH (p)-[:MEMBRE_DE]->(f1:Faction {id: 'generation_terrible'})
   MATCH (p)-[:MEMBRE_DE]->(f2:Faction {id: 'empereurs'})
   WITH p, f1, f2
   ORDER BY p.chapitre
   RETURN p.nom AS Personnage, [f1, f2] AS Factions

### Niveau 3 — Agrégats (30 min)

Doc : Cypher Manual → Aggregation (le GROUP BY implicite).

1. Effectif de chaque équipage, décroissant. -> MATCH (p: Personnage) - [:MEMBRE_DE] -> (e:Equipage)
   RETURN count(p) as effectif, e.nom GROUP BY e ORDER BY effectif DESC
2. Les 15 personnages ayant le plus de relations, toutes relations confondues.
   Ce nombre est le _degré_ du nœud ;
   -> MATCH (p:Personnage)  
    OPTIONAL MATCH (p)-[r]-()  
    RETURN p.nom, count(r) AS degre  
    ORDER BY degre DESC LIMIT 15
3. `collect()` : les mangeurs groupés par type de fruit. -> MATCH (p:Personnage)-[:MANGE]->(f:Fruit)
   RETURN collect(p.nom) as Personnages, f.type as Type
   ORDER BY Type

4. Les degrés de Zoro ET Sanji dans une seule requête
   (indice : `p.nom IN [...]`, puis laisse le regroupement faire le travail).
   -> MATCH (p:Personnage)  
   WHERE p.nom IN ['Roronoa Zoro','Sanji']
   OPTIONAL MATCH (p)-[r]-()  
    RETURN p.nom, count(r) AS degre  
    ORDER BY degre DESC LIMIT 15

### Niveau 4 — Chemins (45 min)

Doc : Cypher Manual → variable-length patterns + shortestPath.

1. Le plus court chemin Luffy ↔ Garp sans emprunter LIE_A.
   -> MATCH p = SHORTEST 1 (a:Personnage {nom : "Monkey D. Luffy"}) - [:MEMBRE_DE | PREMIERE_APPARITION | MANGE] -+ (b:Personnage {nom : 'Monkey D. Garp'})
   RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes, length(p) as distance
2. Idem Luffy ↔ Jewelry Bonney — puis _lis_ le chemin : que raconte-t-il ? -> MATCH p = SHORTEST 1 (a:Personnage {nom : "Monkey D. Luffy"}) - [:MEMBRE_DE | PREMIERE_APPARITION | MANGE] -+ (b:Personnage {nom : 'Jewelry Bonney'})
   RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes, length(p) as distance
3. Tous les chemins de longueur 2 entre Zoro et Sanji.
   MATCH (a:Personnage {nom: "Roronoa Zoro"}), (b:Personnage {nom: "Sanji"})
   MATCH p = (a)-[*2]-(b)
   RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes;

4. Pourquoi la distance structurelle d'usopp-yasopp vaut 4 et pas 2 ?
   → Moralité : le lien père-fils n'est pas déductible des catégories wiki,
   d'où la couche LIE_A. Le graphe structure, l'humain relie.

### Niveau 5 — Le proposeur (le vrai sujet)

1. Les paires LIE_A qui partagent un groupe (l'étalon de validation).
2. Le proposeur : même groupe, pas déjà liées par LIE_A, écart de notoriété
   décroissant. Indices : `NOT (a)-[:LIE_A]-(b)`, `id(a) < id(b)`.
3. Filtre anti-spoil : les liens établis avant l'arc `dressrosa`
   (compare les chapitres de début des deux Arcs).
4. Les paires partageant DEUX groupes — combien sont déjà dans LIE_A ?

## Quand tu bloques

- Erreur la plus fréquente : `WITH is required between ...` — Cypher veut que
  tu fragmentes le pipeline explicitement. C'est une feature : chaque clause
  transforme le jeu de résultats précédent.
- `A pattern expression should only be used ... to test the existence of a
pattern` — tu as mis un motif nu dans un `RETURN`. Un motif n'est pas une
  valeur : demande un booléen avec `exists { (a)-[:LIE_A]-(b) }`, ou une liste
  avec une pattern comprehension `[(a)-[r]-() | r]`.
- `:schema` dans le Browser affiche le méta-graphe (labels, types, propriétés).
- Noms de variables : rien n'est réservé, `r` / `n` / `p` sont de simples
  conventions (relationship, node, path). Attention au faux ami : nos corrigés
  écrivent `p` pour **Personnage**, là où la doc Neo4j écrit `p` pour un
  **chemin** (`MATCH p = shortestPath(...)`). Ne déclare une variable que si
  tu la réutilises ensuite ; sinon `--` ou `-[]-` suffit.
- Une réponse vide n'est pas un bug : c'est une information sur le modèle.
- Requête emballée ? Fermer l'onglet ou couper le client **n'arrête pas** le
  serveur : la transaction continue à mouliner. Le réflexe est
  `SHOW TRANSACTIONS`, repérer l'`elapsedTime` qui grimpe, puis
  `TERMINATE TRANSACTION 'neo4j-transaction-<id>'`.
- Un chemin qui repasse par le même nœud n'est pas un bug : par défaut Cypher
  garantit des **relations** distinctes (mode `TRAIL`), pas des **nœuds**
  distincts. `MATCH p = ACYCLIC (a)-[]-{4}(b)` impose l'unicité des nœuds — à
  préférer dès qu'un chemin doit *expliquer* une proximité. Sur Zoro→Sanji en
  4 sauts : 7 chemins en `TRAIL`, 3 en `ACYCLIC`.
- Quantificateurs de chemin : `{2}` exactement 2 sauts, `{1,3}` de 1 à 3,
  `+` un ou plus **sans borne**, `*` zéro ou plus sans borne. Sans `SHORTEST`,
  les deux derniers énumèrent TOUS les chemins — borne, ou compte d'abord
  avec `{1,n}` croissant avant de lâcher la requête.
- Une syntaxe documentée qui ne passe pas ? Le Cypher Manual « current » suit la
  dernière version, pas la tienne. `CALL dbms.components()` donne le verdict, et
  `SHOW SETTINGS YIELD name, value WHERE name CONTAINS 'default_language'` dit
  quel Cypher t'interprète. On tourne en `2026-community` (Cypher 25 par défaut).
