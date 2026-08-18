"""La manche : la paire tirée et qui a reçu quel personnage.

Le rôle ne vit qu'ici, côté serveur. Chaque joueur ne reçoit que son propre
personnage, sous la même forme pour tous : rien ne distingue l'imposteur, et
ni le lien ni la difficulté ne quittent le serveur avant la révélation.
"""

import random
from dataclasses import dataclass

from jeu.calibrage import pool
from jeu.contrat import Contrat, Paire, Personnage


@dataclass
class Manche:
    """La distribution d'une manche : le duo tiré, et l'imposteur désigné."""

    paire: Paire
    personnage_majorite: Personnage
    personnage_imposteur: Personnage
    imposteur: str
    joueurs: list[str]

    def personnage(self, joueur: str) -> dict:
        """Ce que voit un joueur — identique en forme pour tous."""
        vu = (
            self.personnage_imposteur
            if joueur == self.imposteur
            else self.personnage_majorite
        )
        return {"id": vu.id, "nom": vu.nom}


class Manches:
    """Le stock de paires d'une partie : tirage aléatoire, sans répétition.

    Le stock épuisé se recharge — mieux vaut resservir une paire que refuser
    une manche.
    """

    def __init__(self, contrat: Contrat, calibrage: str):
        self._pool = pool(contrat, calibrage)
        self._personnages = {p.id: p for p in contrat.personnages}
        self._restantes: list[Paire] = []

    def lancer(self, joueurs: list[str]) -> Manche:
        paire = self._tirer()
        return Manche(
            paire=paire,
            personnage_majorite=self._personnages[paire.majorite],
            personnage_imposteur=self._personnages[paire.imposteur],
            imposteur=random.choice(joueurs),
            joueurs=list(joueurs),
        )

    def _tirer(self) -> Paire:
        if not self._restantes:
            self._restantes = list(self._pool)
            random.shuffle(self._restantes)
        return self._restantes.pop()
