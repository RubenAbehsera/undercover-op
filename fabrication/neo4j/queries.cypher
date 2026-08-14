// =============================================================================
// Corrigés commentés des exercices de guide.md.
//
// Méthode : écris TA requête dans le Browser AVANT de lire celle-ci.
//   Browser : http://localhost:7474 (neo4j / mot-de-passe-supprime)
//   Fichier entier :
//     docker exec -i undercover-neo4j cypher-shell -u neo4j -p mot-de-passe-supprime \
//       --format plain < queries.cypher
// =============================================================================


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 1 — Lire : MATCH / WHERE / RETURN / ORDER BY
// Doc : Cypher Manual → clauses MATCH, WHERE, RETURN
// -------------------------------------------------------------------------

// 1.1  Dix personnages.
//      (p:Personnage) : la variable p capture un nœud portant le label.
MATCH (p:Personnage)
RETURN p.nom
LIMIT 10;

// 1.2  Fiche complète de Nami : filtrage par propriété DANS le motif.
//      RETURN p sans projection → le Browser dessine le nœud et ses arêtes.
MATCH (p:Personnage {nom: "Nami"})
RETURN p;

// 1.3  Les vétérans d'East Blue. WHERE filtre le motif — l'équivalent SQL
//      filtre des lignes de table ; ici on filtre des nœuds / chemins.
MATCH (p:Personnage)
WHERE p.chapitre < 50
RETURN p.nom, p.chapitre, p.arc
ORDER BY p.chapitre;

// 1.4  Fruits Zoan. CONTAINS = sous-chaîne, insensible à la casse. On ne peut
//      pas tester l'égalité : les types sont bruts du wiki (« Zoan »,
//      « Ancient Zoan », « Paramecia ( Mythical Zoan ) »…). Le nettoyage de
//      ces valeurs est un travail de fabrication, pas de requête.
MATCH (f:Fruit)
WHERE f.type CONTAINS "Zoan"
RETURN f.nom, f.type;


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 2 — Motifs : les relations sont de l'ASCII-art
// Doc : Cypher Manual → Patterns
//   (a)-[:REL]->(b)  orienté      (a)-[:REL]-(b)  non orienté
// -------------------------------------------------------------------------

// 2.1  Les groupes de Jinbe. Un même type MEMBRE_DE pointe vers des Equipage
//      ET des Faction : labels() les distingue.
MATCH (:Personnage {nom: "Jinbe"})-[:MEMBRE_DE]->(g)
RETURN labels(g)[0] AS nature, g.nom;

// 2.2  L'équipage fondateur, par ordre d'arrivée dans le manga.
MATCH (p:Personnage)-[:MEMBRE_DE]->(:Equipage {id: "straw_hat_pirates"})
RETURN p.nom, p.chapitre
ORDER BY p.chapitre;

// 2.3  Qui mange quoi : DEUX motifs dans un MATCH, reliés par la variable p
//      partagée — c'est le JOIN du graphe, et il se lit comme une phrase.
MATCH (p:Personnage)-[:MEMBRE_DE]->(:Equipage {id: "straw_hat_pirates"}),
      (p)-[:MANGE]->(f:Fruit)
RETURN p.nom, f.nom;

// 2.4  Le croisement : deux motifs successifs = ET logique.
MATCH (p:Personnage)-[:MEMBRE_DE]->(:Faction {id: "generation_terrible"})
MATCH (p)-[:MEMBRE_DE]->(:Faction {id: "empereurs"})
RETURN p.nom;


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 3 — Agrégats : le GROUP BY est implicite
// Doc : Cypher Manual → Aggregation
// Règle : les colonnes NON agrégées du RETURN forment la clé de regroupement.
// Depuis 2026.07.0 un GROUP BY explicite existe aussi (alignement GQL) ; il
// est optionnel et ne change pas la règle ci-dessus. Voir la variante en 3.1.
// -------------------------------------------------------------------------

// 3.1  Effectifs. count(p) regroupe par g.nom, seule colonne non agrégée.
MATCH (g:Equipage)<-[:MEMBRE_DE]-(p:Personnage)
RETURN g.nom, count(p) AS effectif
ORDER BY effectif DESC;

// 3.1 bis  La même, clé de regroupement déclarée. Utile quand le RETURN est
//          long : la clé devient lisible au lieu d'être déduite de ce qui
//          reste. Erreur de syntaxe avant 2026.07.0 — vérifie ta version
//          avec CALL dbms.components() avant de croire le Cypher Manual.
MATCH (p:Personnage)-[:MEMBRE_DE]->(e:Equipage)
RETURN e.nom AS equipage, count(p) AS effectif
GROUP BY e.nom
ORDER BY effectif DESC;

// 3.2  LA notoriété. -[r]- (sans flèche) = toute relation, tout sens.
//      OPTIONAL MATCH : garde les nœuds sans relations (degré 0) au lieu
//      de les éliminer silencieusement — l'équivalent du LEFT JOIN.
MATCH (p:Personnage)
OPTIONAL MATCH (p)-[r]-()
RETURN p.nom, count(r) AS degre
ORDER BY degre DESC LIMIT 15;

// 3.3  collect() transforme le groupe en liste (l'inverse : UNWIND).
//      Le regroupement se fait sur f.type, colonne non agrégée.
MATCH (p:Personnage)-[:MANGE]->(f:Fruit)
RETURN f.type AS type, collect(p.nom) AS mangeurs
ORDER BY size(mangeurs) DESC;

// 3.4  Zoro et Sanji d'un coup : WHERE ... IN, puis le regroupement par p.nom
//      fait le reste. Un seul motif, zéro UNION.
MATCH (p:Personnage)
WHERE p.nom IN ["Roronoa Zoro", "Sanji"]
OPTIONAL MATCH (p)-[r]-()
RETURN p.nom, count(r) AS degre;


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 4 — Chemins : là où le graphe écrase le relationnel
// Doc : Cypher Manual → variable-length patterns, shortestPath
//   -[:MEMBRE_DE|PREMIERE_APPARITION|MANGE*..6]-   1 à 6 sauts, types au choix
// -------------------------------------------------------------------------

// 4.1  Plus court chemin Luffy ↔ Garp SANS LIE_A. En restreignant les types
//      dans le motif, LIE_A n'est même pas candidate. Variante générique,
//      quand on ne peut pas lister les types :
//        WHERE none(rel IN relationships(p) WHERE type(rel) = "LIE_A")
MATCH (a:Personnage {nom: "Monkey D. Luffy"}), (b:Personnage {nom: "Monkey D. Garp"})
MATCH p = shortestPath((a)-[:MEMBRE_DE|PREMIERE_APPARITION|MANGE*..6]-(b))
RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes, length(p) AS distance;

// 4.1 bis  La même en syntaxe GQL de Cypher 25 : SHORTEST k remplace
//          shortestPath(), et le quantificateur '+' (1 saut ou plus) remplace
//          '*..6'. Les deux formes coexistent sur 2026.x ; la doc « current »
//          ne montre plus que celle-ci, d'où le dépaysement quand on lit le
//          Cypher Manual avec nos corrigés sous les yeux.
MATCH p = SHORTEST 1 (a:Personnage {nom: "Monkey D. Luffy"})
          -[:MEMBRE_DE|PREMIERE_APPARITION|MANGE]-+
          (b:Personnage {nom: "Monkey D. Garp"})
RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes, length(p) AS distance;

// 4.2  Luffy ↔ Bonney : lis le chemin à voix haute — « Luffy appartient à la
//      Génération Terrible, Bonney aussi ». Deux sauts, l'équerre du graphe.
MATCH (a:Personnage {nom: "Monkey D. Luffy"}), (b:Personnage {nom: "Jewelry Bonney"})
MATCH p = shortestPath((a)-[:MEMBRE_DE|PREMIERE_APPARITION|MANGE*..6]-(b))
RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes, length(p) AS distance;

// 4.3  Longueur EXACTEMENT 2 entre Zoro et Sanji : leurs points communs.
//      Une seule ligne : l'équipage. Pas d'arc commun (Romance Dawn vs
//      Baratie), pas de fruit commun. Une réponse courte EST une information.
MATCH (a:Personnage {nom: "Roronoa Zoro"}), (b:Personnage {nom: "Sanji"})
MATCH p = (a)-[*2]-(b)
RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes;

// 4.4  Pourquoi 4 pour usopp-yasopp ? Aucun arc commun, aucun groupe commun :
//      le lien père-fils n'existe nulle part dans les catégories wiki, le
//      chemin doit contourner (Usopp → équipage → Luffy → faction → Shanks
//      → Roger Pirates → Yasopp, à quelques variantes près).
//      PREUVE que LIE_A est indispensable : le graphe structure, l'humain relie.
MATCH (a:Personnage {nom: "Usopp"}), (b:Personnage {nom: "Yasopp"})
MATCH p = shortestPath((a)-[:MEMBRE_DE|PREMIERE_APPARITION|MANGE*..6]-(b))
RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes, length(p) AS distance;


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 5 — Le proposeur : la requête métier de la fabrication
// Doc : Cypher Manual → négation de motifs, pattern comprehension
// -------------------------------------------------------------------------

// 5.1  L'étalon : quelles paires LIE_A ont un support structurel ?
//      (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b) = le motif « nœud partagé »,
//      l'équerre du graphe.
//      id(a) < id(b) : un match non orienté produit les DEUX orientations
//      (a,b) et (b,a) — comparer les ids internes déduplique. Idiome standard.
MATCH (a:Personnage)-[l:LIE_A]-(b:Personnage)
WHERE id(a) < id(b)
OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
WITH a, b, l, collect(DISTINCT g.nom) AS groupes
WHERE size(groupes) > 0
RETURN a.nom AS majorite, b.nom AS imposteur, l.type AS type, groupes
ORDER BY size(groupes) DESC;

// 5.2  LE proposeur : deux membres d'un même groupe, pas déjà liés, écart de
//      notoriété maximal — la majorité doit être connue, l'imposteur moins.
//        NOT (a)-[:LIE_A]-(b) : négation d'un MOTIF (impossible en SQL pur).
//        [(a)-[r]-() | r]     : pattern comprehension, toutes les relations
//                              de a dans une liste — le degré, avant la mue.
MATCH (a:Personnage)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b:Personnage)
WHERE id(a) < id(b) AND NOT (a)-[:LIE_A]-(b)
WITH a, b, g,
     [(a)-[r]-() | r] AS ra,
     [(b)-[r]-() | r] AS rb
RETURN a.nom AS majorite, b.nom AS imposteur, g.nom AS groupe,
       size(ra) AS deg_a, size(rb) AS deg_b, size(ra) - size(rb) AS ecart
ORDER BY ecart DESC
LIMIT 12;

// 5.3  Anti-spoil : uniquement les liens établis avant l'arc de calibrage.
//      Deux Arcs comparés par leur chapitre de début (propriétés debut/fin).
//      C'est exactement la règle « arc d'établissement ≤ calibrage » du jeu.
MATCH (a:Personnage)-[l:LIE_A]->(b:Personnage)
MATCH (calibrage:Arc {id: "dressrosa"})
MATCH (lien:Arc {id: l.arc})
WHERE lien.debut <= calibrage.debut
RETURN a.nom, b.nom, l.type, l.arc AS arc_du_lien
ORDER BY lien.debut;

// 5.4  Deux groupes partagés : les paires les plus faciles à relier pour un
//      joueur (buggy-shanks : Roger Pirates + Empereurs). Combien sont déjà
//      dans LIE_A ? Ce sont les premières validées par le graphe.
//      Piège Neo4j 5 : un motif nu dans le RETURN est refusé (« A pattern
//      expression should only be used in order to test the existence of a
//      pattern »). Un motif n'est pas une valeur : pour en tirer un booléen il
//      faut le demander, avec la sous-requête EXISTS { }.
MATCH (a:Personnage)-[:MEMBRE_DE]->(g1)<-[:MEMBRE_DE]-(b:Personnage),
      (a)-[:MEMBRE_DE]->(g2)<-[:MEMBRE_DE]-(b)
WHERE id(a) < id(b) AND id(g1) < id(g2)
RETURN a.nom, b.nom, g1.nom AS groupe_1, g2.nom AS groupe_2,
       exists { (a)-[:LIE_A]-(b) } AS deja_lie
ORDER BY deja_lie DESC
LIMIT 10;
