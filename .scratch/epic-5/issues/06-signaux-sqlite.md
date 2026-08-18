# 06 — Les signaux → SQLite

**What to build:** La mesure, persistée en SQLite mono-fichier (stdlib, pas d'ORM). Signal objectif par manche, écrit à la révélation : imposteur démasqué ou non, nombre de tours, répartition des votes. Drapeau « je ne connais pas » : par joueur et par manche, strictement confidentiel, définitif pour la manche, et une manche qui le porte est exclue du calcul de qualité des tirages. Signal subjectif en fin de partie : trois niveaux en un tap, commentaire optionnel — déclenché par la fin de partie décidée par l'hôte.

**Blocked by:** 04 — La manche : machine à états · 05 — Cycle de vie room & partie.

**Status:** ready-for-agent

- [ ] Chaque manche terminée écrit sa ligne de signal objectif en SQLite
- [ ] Drapeau « je ne connais pas » : absent de tous les payloads (confidentiel), définitif pour la manche
- [ ] Une manche portant le drapeau est exclue du calcul de qualité des tirages
- [ ] Fin de partie → signal subjectif (trois niveaux, commentaire optionnel) enregistré
