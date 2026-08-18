# 05 — Cycle de vie room & partie

**What to build:** Les règles de vie d'une room au long cours. Un joueur qui part en cours de manche est conservé dans l'état et sauté à l'ordre de parole — il ne bloque ni les tours ni le vote. Départ de l'hôte : transfert au joueur le plus ancien, les contrôles de flux suivent. La partie est terminée par l'hôte (c'est ce qui déclenchera le feedback, ticket 06). Une room est supprimée après 2 h d'inactivité. *(US 5.7, seconde moitié)*

**Blocked by:** 04 — La manche : machine à états.

**Status:** ready-for-agent

- [ ] Départ d'un joueur en cours de manche : conservé dans l'état, sauté à l'ordre de parole, tours et vote non bloqués
- [ ] Départ de l'hôte : transfert au joueur le plus ancien, contrôles de flux opérationnels
- [ ] Fin de partie décidée par l'hôte : signal de fin émis à tous
- [ ] Room inactive depuis 2 h → supprimée (testable sans attendre : horloge injectable)
