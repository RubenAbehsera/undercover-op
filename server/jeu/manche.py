"""La manche : la paire tirée et qui a reçu quel personnage.

Le rôle ne vit qu'ici, côté serveur. Chaque joueur ne reçoit que son propre
personnage, sous la même forme pour tous : rien ne distingue l'imposteur, et
ni le lien ni la difficulté ne quittent le serveur avant la révélation.
"""

import random
from collections import Counter
from dataclasses import dataclass, field
from typing import Literal

from jeu.calibrage import pool
from jeu.contrat import Contrat, Paire, Personnage
from jeu.erreurs import ErreurRoom

Etat = Literal["paroles", "vote", "revelation"]


def fiche(personnage: Personnage) -> dict:
    """Un personnage tel que le client le voit — son nom, et rien de plus."""
    return {"id": personnage.id, "nom": personnage.nom}


@dataclass
class Manche:
    """La distribution d'une manche : le duo tiré, et l'imposteur désigné."""

    paire: Paire
    personnage_majorite: Personnage
    personnage_imposteur: Personnage
    imposteur: str
    joueurs: list[str]
    ordre: list[str] = field(default_factory=list)
    etat: Etat = "paroles"
    tour: int = 1
    position: int = 0
    votes: dict[str, str] = field(default_factory=dict)
    partis: set[str] = field(default_factory=set)
    meconnaissances: set[str] = field(default_factory=set)
    consignee: bool = False

    def en_cours(self) -> bool:
        """Tant que la révélation n'est pas là, la manche occupe la room."""
        return self.etat != "revelation"

    def presents(self) -> list[str]:
        return [joueur for joueur in self.joueurs if joueur not in self.partis]

    def ordre_present(self) -> list[str]:
        """L'ordre de parole tel qu'il tourne vraiment — sans les partis."""
        return [joueur for joueur in self.ordre if joueur not in self.partis]

    def retirer(self, joueur: str) -> None:
        """Un départ en cours de manche : le joueur reste connu, mais sauté."""
        self.partis.add(joueur)
        if self.etat == "paroles":
            self._sauter_les_partis()

    def orateur(self) -> str:
        return self.ordre[self.position]

    def passer(self, joueur: str) -> None:
        """L'orateur rend la parole ; le tour suivant s'ouvre au bout du cycle."""
        if joueur != self.orateur():
            raise ErreurRoom("pas_ton_tour", "ce n'est pas à vous de parler")
        self._avancer()
        self._sauter_les_partis()

    def _avancer(self) -> None:
        self.position += 1
        if self.position == len(self.ordre):
            self.position = 0
            self.tour += 1

    def _sauter_les_partis(self) -> None:
        """Un absent ne retient pas la parole — on passe au suivant présent."""
        for _ in range(len(self.ordre)):
            if self.ordre[self.position] not in self.partis:
                return
            self._avancer()

    def tours_joues(self) -> int:
        """Les tours où l'on a parlé — le tour courant compte s'il est entamé."""
        return self.tour if self.position else self.tour - 1

    def ouvrir_vote(self) -> None:
        """L'hôte arrête les tours de parole et ouvre la consultation."""
        if self.etat != "paroles":
            raise ErreurRoom("vote_impossible", "le vote a déjà eu lieu")
        self.etat = "vote"

    def voter(self, votant: str, cible: str) -> None:
        if self.etat != "vote":
            raise ErreurRoom("pas_de_vote", "aucun vote en cours")
        if votant == cible:
            raise ErreurRoom("vote_pour_soi", "on ne vote pas pour soi")
        if cible not in self.presents():
            raise ErreurRoom("cible_inconnue", f"joueur hors manche : {cible}")
        if votant in self.votes:
            raise ErreurRoom("deja_vote", "vous avez déjà voté")
        self.votes[votant] = cible

    def tous_ont_vote(self) -> bool:
        """Les partis ne sont plus attendus — seuls les présents ferment le vote."""
        return all(joueur in self.votes for joueur in self.presents())

    def fermer_vote(self) -> None:
        self.etat = "revelation"

    def designe(self) -> str | None:
        """Le joueur qui réunit la majorité stricte des suffrages exprimés.

        Sans majorité stricte, personne n'est désigné — et l'imposteur l'emporte.
        """
        if not self.votes:
            return None
        cible, voix = Counter(self.votes.values()).most_common(1)[0]
        return cible if voix * 2 > len(self.votes) else None

    def demasque(self) -> bool:
        return self.designe() == self.imposteur

    def repartition(self) -> list[int]:
        """Comment les suffrages se sont massés — des effectifs, pas des noms.

        La mesure veut savoir si le groupe s'est rangé derrière une cible ou
        s'est éparpillé ; qui a voté pour qui ne la regarde pas.
        """
        return sorted(Counter(self.votes.values()).values(), reverse=True)

    def voix_imposteur(self) -> int:
        return sum(1 for cible in self.votes.values() if cible == self.imposteur)

    def signaler_meconnaissance(self, joueur: str) -> None:
        """« Je ne connais pas ce personnage » — confidentiel et sans retour.

        Rien n'en sort : ni diffusion, ni trace dans un payload. La manche qui
        en porte un sera écartée du calcul de qualité des tirages.
        """
        if self.etat == "revelation":
            raise ErreurRoom("manche_terminee", "la manche est terminée")
        if joueur in self.meconnaissances:
            raise ErreurRoom("deja_signale", "le drapeau est déjà levé")
        self.meconnaissances.add(joueur)

    def personnage(self, joueur: str) -> dict:
        """Ce que voit un joueur — identique en forme pour tous."""
        vu = (
            self.personnage_imposteur
            if joueur == self.imposteur
            else self.personnage_majorite
        )
        return fiche(vu)


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
            ordre=random.sample(joueurs, k=len(joueurs)),
        )

    def _tirer(self) -> Paire:
        if not self._restantes:
            self._restantes = list(self._pool)
            random.shuffle(self._restantes)
        return self._restantes.pop()
