# Parcours Neo4j — apprendre sur notre graphe

Objectif : disposer des requêtes de fabrication (validation des paires,
proposeur, score) écrites et vérifiées. Les niveaux 1 à 5 ont servi
d'apprentissage — réponses inline, corrigés dans `queries.cypher` ; à partir
du niveau 6, les requêtes vivent en clair ici et sont tenues à jour par
l'agent, en synchronisation avec `queries.cypher` (numérotation identique).
Le graphe est **jetable** : tout se régénère depuis les seeds. Casse-le sans
peur.

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

`LIE_A` est la couche humaine (les 24 paires figées) ; tout le reste vient
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

Niveaux 1 à 5 — le parcours d'apprentissage : lis la doc → fais les exos dans
le Browser → compare avec le corrigé commenté dans `queries.cypher`
(même numéro). À partir du niveau 6 : de la référence directe, requêtes en
clair, plus d'exercice.

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
   -> MATCH (a:Personnage)-[l:LIE_A]-(b:Personnage)
   WHERE elementId(a) < elementId(b)
   OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
   WITH a, b, l, collect(DISTINCT g.nom) AS groupes
   WHERE size(groupes) > 0
   RETURN a.nom AS majorite, b.nom AS imposteur, l.type AS type, groupes
   ORDER BY size(groupes) DESC;
2. Le proposeur : même groupe, pas déjà liées par LIE_A, écart de notoriété
   décroissant. Indices : `NOT (a)-[:LIE_A]-(b)`, `id(a) < id(b)`.
   MATCH (a:Personnage)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b:Personnage)
   WHERE elementId(a) < elementId(b) AND NOT (a)-[:LIE_A]-(b)
   WITH a, b, g,
   [(a)-[r]-() | r] AS ra,
   [(b)-[r]-() | r] AS rb
   RETURN a.nom AS majorite, b.nom AS imposteur, g.nom AS groupe,
   size(ra) AS deg_a, size(rb) AS deg_b, size(ra) - size(rb) AS ecart
   ORDER BY ecart DESC
   LIMIT 12;
3. Filtre anti-spoil : les liens établis avant l'arc `dressrosa`
   (compare les chapitres de début des deux Arcs).
   MATCH (a:Personnage)-[l:LIE_A]->(b:Personnage)
   MATCH (calibrage:Arc {id: "dressrosa"})
   MATCH (lien:Arc {id: l.arc})
   WHERE lien.debut <= calibrage.debut
   RETURN a.nom, b.nom, l.type, l.arc AS arc_du_lien
   ORDER BY lien.debut;
4. Les paires partageant DEUX groupes — combien sont déjà dans LIE_A ?
   MATCH (a:Personnage)-[:MEMBRE_DE]->(g1)<-[:MEMBRE_DE]-(b:Personnage),
   (a)-[:MEMBRE_DE]->(g2)<-[:MEMBRE_DE]-(b)
   WHERE elementId(a) < elementId(b) AND elementId(g1) < elementId(g2)
   RETURN a.nom, b.nom, g1.nom AS groupe_1, g2.nom AS groupe_2,
   exists { (a)-[:LIE_A]-(b) } AS deja_lie
   ORDER BY deja_lie DESC
   LIMIT 10;

### Niveau 6 — Écrire dans le graphe (référence)

La fabrication écrit dans le graphe pour deux choses : matérialiser un calcul
pour ne pas le refaire à chaque requête, et charger un lot en paramètre.

**6.1 — Notoriété.** La pattern comprehension dans le `SET` : zéro agrégat,
zéro sous-requête. Désormais les requêtes aval lisent `p.notoriete` comme une
propriété ordinaire.

    MATCH (p:Personnage)
    SET p.notoriete = size([(p)-[r]-() | r]);

**6.2 — Normalisation 0–100.** Après un `WITH` d'agrégat, on repart d'UNE
ligne pour re-parcourir. `100.0` et pas `100` : entier / entier = division
entière.

    MATCH (p:Personnage)
    WITH max(p.notoriete) AS maxi
    MATCH (q:Personnage)
    SET q.notoriete_norm = toInteger(round(100.0 * q.notoriete / maxi));

**6.3 — Lot en paramètre.** `UNWIND`, l'inverse de `collect()`. Changer
d'étalon = changer le `:param`, pas la requête. Orientation : majorite
d'abord.

    :param etalon => [{a: 'roronoa_zoro', b: 'kuina'}, {a: 'usopp', b: 'yasopp'},
                      {a: 'sanji', b: 'zeff'}, {a: 'shanks', b: 'buggy'}]

    UNWIND $etalon AS e
    MATCH (a:Personnage {id: e.a})-[l:LIE_A]->(b:Personnage {id: e.b})
    OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
    RETURN e.a + ' / ' + e.b AS paire, l.type AS type,
           collect(DISTINCT g.nom) AS groupes;

**6.4 — MERGE vs CREATE.** MERGE = trouve-ou-créé sur le motif **complet** ;
c'est lui qui rend `neo4j_import.py` rejouable. Piège : un MERGE partiel
(label seul) suivi d'un `SET` des propriétés duplique à chaque exécution —
ce qui identifie va DANS le MERGE, le reste dans `ON CREATE SET`. La démo
CREATE/MERGE/DETACH DELETE vit en 6.4 dans `queries.cypher`.

### Niveau 7 — Le score et le test de passage (référence)

L'assemblage 5.1 + 5.2 + 5.3 (+ 6.1) — le cœur du jalon 3. `LIE_A` est
orientée majorite → imposteur à l'import : le `MATCH` dirigé rend chaque
paire exactement une fois, dans le bon sens (le `elementId(a) < elementId(b)`
du 5.1 ne sert plus).

**7.1 — La fiche.** Une ligne par paire : notoriétés, écart, support, chapitre
d'établissement. Un écart négatif n'est pas un bug — l'imposteur mieux
connecté que la majorité, c'est une information.

    MATCH (a:Personnage)-[l:LIE_A]->(b:Personnage)
    OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
    MATCH (arc:Arc {id: l.arc})
    WITH a, b, l, arc, collect(DISTINCT g.nom) AS groupes
    RETURN a.nom AS majorite, b.nom AS imposteur, l.type AS type,
           a.notoriete AS deg_maj, b.notoriete AS deg_imp,
           a.notoriete - b.notoriete AS ecart, size(groupes) AS support,
           arc.debut AS etabli_au_chapitre
    ORDER BY ecart DESC;

**7.2 — Le score.** Trois signaux, tous structurels : le graphe seul note.
`l.difficulte` est exclue : humaine, elle transformerait le test en
tautologie. Les coefficients sont des **hypothèses de départ** — le réglage
se fera contre l'étalon (7.3) en bougeant ces nombres.

    MATCH (a:Personnage)-[l:LIE_A]->(b:Personnage)
    OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
    MATCH (arc:Arc {id: l.arc}), (calibrage:Arc {id: 'dressrosa'})
    WITH a, b, l, arc, calibrage, collect(DISTINCT g.nom) AS groupes
    WITH a, b, l,
         a.notoriete - b.notoriete AS ecart,
         size(groupes) AS support,
         arc.debut <= calibrage.debut AS precoce
    RETURN a.nom AS majorite, b.nom AS imposteur, l.type AS type,
           ecart, support, precoce,
           CASE WHEN ecart > 10 THEN 25 WHEN ecart > 4 THEN 15 ELSE 5 END
           + support * 15
           + CASE WHEN precoce THEN 10 ELSE 0 END AS score
    ORDER BY score DESC;

**7.3 — Le test de passage.** Toutes les paires dans une liste (`collect`),
puis `UNWIND` pour re-déplier. Le rang d'une paire = nombre de scores
strictement supérieurs + 1 ; les ex æquo partagent leur rang (1-2-2-4).
L'étalon est figé : les 24 paires du lot entier (2026-08-18) — le contrôle
devient la relecture humaine du classement complet.

    :param etalon_ids => ['roronoa_zoro|kuina', 'usopp|yasopp',
                          'sanji|zeff', 'shanks|buggy']

    MATCH (a:Personnage)-[l:LIE_A]->(b:Personnage)
    OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
    MATCH (arc:Arc {id: l.arc}), (calibrage:Arc {id: 'dressrosa'})
    WITH a, b, arc, calibrage, collect(DISTINCT g.nom) AS groupes
    WITH a.id + '|' + b.id AS cle, a.nom + ' / ' + b.nom AS paire,
         CASE WHEN a.notoriete - b.notoriete > 10 THEN 25
              WHEN a.notoriete - b.notoriete > 4 THEN 15 ELSE 5 END
         + size(groupes) * 15
         + CASE WHEN arc.debut <= calibrage.debut THEN 10 ELSE 0 END AS score
    WITH collect({cle: cle, paire: paire, score: score}) AS classement
    UNWIND classement AS c
    WITH c, [autre IN classement WHERE autre.score > c.score | 1] AS devant
    RETURN size(devant) + 1 AS rang, c.paire AS paire, c.score AS score,
           c.cle IN $etalon_ids AS etalon
    ORDER BY rang, paire;

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
  préférer dès qu'un chemin doit _expliquer_ une proximité. Sur Zoro→Sanji en
  4 sauts : 7 chemins en `TRAIL`, 3 en `ACYCLIC`.
- Quantificateurs de chemin : `{2}` exactement 2 sauts, `{1,3}` de 1 à 3,
  `+` un ou plus **sans borne**, `*` zéro ou plus sans borne. Sans `SHORTEST`,
  les deux derniers énumèrent TOUS les chemins — borne, ou compte d'abord
  avec `{1,n}` croissant avant de lâcher la requête.
- Une syntaxe documentée qui ne passe pas ? Le Cypher Manual « current » suit la
  dernière version, pas la tienne. `CALL dbms.components()` donne le verdict, et
  `SHOW SETTINGS YIELD name, value WHERE name CONTAINS 'default_language'` dit
  quel Cypher t'interprète. On tourne en `2026-community` (Cypher 25 par défaut).
