# 01 — Charger le contrat au démarrage

**What to build:** Le serveur démarre et ne connaît du domaine One Piece que le contrat figé `fabrication/paires.json`. Au lancement, il charge le fichier et le valide intégralement via un schéma Pydantic v2 : arcs canoniques ordonnés, personnages (id, nom, arc_premiere_apparition, notoriete), paires (majorite, imposteur, lien type + libellé, difficulte, arc_etablissement) — références croisées vérifiées (chaque personnage cité existe, chaque arc cité est dans la liste canonique, difficulte dans l'enum). Fichier absent ou invalide : erreur nette qui nomme le défaut, arrêt propre — jamais de serveur lancé sur un contrat bancal. Livre le squelette du service : FastAPI + python-socketio async dans un seul process ASGI, prêt à recevoir les événements des tickets suivants. *(US 5.1)*

**Blocked by:** None — can start immediately.

**Status:** ready-for-agent

- [x] Le serveur démarre avec le contrat figé et le tient validé en mémoire (prêt pour le tirage)
- [x] Fichier absent : message d'erreur net au démarrage, arrêt propre
- [x] Fichier invalide (champ manquant, référence cassée, difficulte hors enum, arc inconnu) : l'erreur nomme précisément le défaut
- [x] Test de validation rejouable sur le contrat réel des 24 paires

## Comments

- **2026-08-18, commit f478a6d** — implémenté TDD (10 tests verts), revue deux axes passée
  (correctifs : .gitignore réparé — un `>>` sans newline final avait fusionné `.claude/` et
  `jeu.egg-info/` ; helper `_inconnu` ; fixture `chemin_contrat` ; deux branches non couvertes
  testées : arc de première apparition d'un personnage, exit 1 du process). Démo live : avec le
  contrat `/sante` répond `{"etat": "ok"}` ; sans lui, message net + code sortie 1. Refusés en
  revue : vérifier l'ordre canonique des arcs (tautologique — le fichier est la source de
  vérité) ; `api.state.contrat` conservé (sert « prêt pour le tirage », le ticket 02 y branchera
  les événements socket).
