"""La vie des rooms hors manche : création, salle d'attente, arrivées et départs.

L'identité réelle d'un joueur est son ID opaque (localStorage) ; le pseudo n'est
que l'affichage. La salle d'attente ne publie donc que des pseudos — uniques
dans la room, ils suffisent à désigner qui que ce soit sans divulguer d'ID.
"""

import random
import time
from dataclasses import dataclass, field

from jeu.calibrage import arcs_proposes
from jeu.contrat import Contrat
from jeu.erreurs import ErreurRoom
from jeu.manche import Manche, Manches, fiche

PLAFOND = 12
MINIMUM = 3
INACTIVITE = 2 * 60 * 60
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
PSEUDO_MINIMUM = 2
LONGUEUR_CODE = 4


@dataclass
class Joueur:
    id: str
    pseudo: str
    present: bool = True


@dataclass
class Room:
    code: str
    calibrage: str
    hote: str
    manches: Manches
    joueurs: list[Joueur] = field(default_factory=list)
    manche: Manche | None = None
    terminee: bool = False
    activite: float = 0.0

    def tour(self) -> dict:
        """Qui parle, dans quel ordre, à quel tour — public, en pseudos."""
        return {
            "ordre": [self._pseudo(joueur) for joueur in self.manche.ordre_present()],
            "orateur": self._pseudo(self.manche.orateur()),
            "tour": self.manche.tour,
        }

    def vote_ouvert(self) -> dict:
        """Le bulletin : pour qui l'on peut voter — chacun s'y trouve aussi."""
        return {"joueurs": [self._pseudo(joueur) for joueur in self.manche.presents()]}

    def revelation(self) -> dict:
        """Tout ce que la manche avait caché — sauf la difficulté de la paire."""
        manche = self.manche
        designe = manche.designe()
        return {
            "majorite": fiche(manche.personnage_majorite),
            "imposteur": fiche(manche.personnage_imposteur),
            "joueur_imposteur": self._pseudo(manche.imposteur),
            "lien": manche.paire.lien.libelle,
            "votes": [
                {"votant": self._pseudo(votant), "cible": self._pseudo(cible)}
                for votant, cible in manche.votes.items()
            ],
            "designe": self._pseudo(designe) if designe else None,
            "demasque": manche.demasque(),
            "tours": manche.tours_joues(),
        }

    def salle_attente(self) -> dict:
        return {
            "code": self.code,
            "calibrage": self.calibrage,
            "hote": self._pseudo(self.hote),
            "joueurs": [joueur.pseudo for joueur in self.presents()],
        }

    def presents(self) -> list[Joueur]:
        """Les joueurs encore connectés — un parti reste dans l'état, pas ici."""
        return [joueur for joueur in self.joueurs if joueur.present]

    def absenter(self, id_joueur: str) -> None:
        for joueur in self.joueurs:
            if joueur.id == id_joueur:
                joueur.present = False

    def id_de(self, pseudo: str) -> str:
        for joueur in self.presents():
            if joueur.pseudo == pseudo:
                return joueur.id
        raise ErreurRoom("cible_inconnue", f"pseudo hors room : {pseudo}")

    def _pseudo(self, id_joueur: str) -> str | None:
        for joueur in self.joueurs:
            if joueur.id == id_joueur:
                return joueur.pseudo
        return None


class Rooms:
    """Les rooms vivantes, en mémoire — le serveur est l'unique source de vérité."""

    def __init__(self, contrat: Contrat, generer_code=None, horloge=time.monotonic):
        self.arcs_proposes = arcs_proposes(contrat)
        self._contrat = contrat
        self._rooms: dict[str, Room] = {}
        self._generer_code = generer_code or _code_aleatoire
        self._horloge = horloge

    def creer(self, joueur: str, pseudo: str, calibrage: str) -> Room:
        self._purger()
        if calibrage not in self.arcs_proposes:
            raise ErreurRoom("calibrage_inconnu", f"calibrage inconnu : {calibrage}")
        hote = Joueur(id=joueur, pseudo=_pseudo_valide(pseudo))
        room = Room(
            code=self._code_libre(),
            calibrage=calibrage,
            hote=joueur,
            manches=Manches(self._contrat, calibrage),
            activite=self._horloge(),
        )
        room.joueurs.append(hote)
        self._rooms[room.code] = room
        return room

    def rejoindre(self, code: str, joueur: str, pseudo: str) -> Room:
        room = self.room(code)
        pseudo = _pseudo_valide(pseudo)
        if any(present.id == joueur for present in room.joueurs):
            return room
        _verifier_partie_ouverte(room)
        if room.manche is not None and room.manche.en_cours():
            raise ErreurRoom("manche_en_cours", "on ne rejoint qu'entre les manches")
        if len(room.joueurs) >= PLAFOND:
            raise ErreurRoom("room_pleine", f"la room est pleine ({PLAFOND} joueurs)")
        if any(present.pseudo.casefold() == pseudo.casefold() for present in room.joueurs):
            raise ErreurRoom("pseudo_pris", f"pseudo déjà pris : {pseudo}")
        room.joueurs.append(Joueur(id=joueur, pseudo=pseudo))
        return room

    def quitter(self, code: str, joueur: str) -> Room | None:
        """Retire le joueur ; renvoie la room, ou None si elle n'existe plus.

        En cours de manche, le parti est conservé dans l'état — son pseudo doit
        survivre jusqu'à la révélation — mais il ne retient plus rien.
        """
        room = self._rooms.get(code)
        if room is None:
            return None
        if room.manche is not None and room.manche.en_cours():
            room.absenter(joueur)
            room.manche.retirer(joueur)
            if room.manche.etat == "vote" and room.manche.tous_ont_vote():
                room.manche.fermer_vote()
        else:
            room.joueurs = [reste for reste in room.joueurs if reste.id != joueur]
        if not room.presents():
            del self._rooms[code]
            return None
        if room.hote == joueur:
            room.hote = room.presents()[0].id
        return room

    def lancer_manche(self, code: str, joueur: str) -> Manche:
        """L'hôte distribue les rôles ; le stock de la room fournit la paire.

        C'est ici que les partis de la manche précédente sortent de l'état.
        """
        room = self.room(code)
        _verifier_hote(room, joueur)
        _verifier_partie_ouverte(room)
        if room.manche is not None and room.manche.en_cours():
            raise ErreurRoom("manche_en_cours", "une manche est déjà en cours")
        room.joueurs = room.presents()
        if len(room.joueurs) < MINIMUM:
            raise ErreurRoom(
                "joueurs_insuffisants", f"il faut au moins {MINIMUM} joueurs"
            )
        room.manche = room.manches.lancer([present.id for present in room.joueurs])
        return room.manche

    def passer_parole(self, code: str, joueur: str) -> Room:
        """L'orateur rend la parole — les tours ne sont pas un contrôle d'hôte."""
        room = self._en_manche(code)
        room.manche.passer(joueur)
        return room

    def ouvrir_vote(self, code: str, joueur: str) -> Room:
        room = self._en_manche(code)
        _verifier_hote(room, joueur)
        room.manche.ouvrir_vote()
        return room

    def voter(self, code: str, joueur: str, cible: str) -> Room:
        """La cible est désignée par son pseudo — les ID restent au serveur."""
        room = self._en_manche(code)
        room.manche.voter(joueur, room.id_de(cible))
        if room.manche.tous_ont_vote():
            room.manche.fermer_vote()
        return room

    def forcer_vote(self, code: str, joueur: str) -> Room:
        room = self._en_manche(code)
        _verifier_hote(room, joueur)
        room.manche.fermer_vote()
        return room

    def terminer_partie(self, code: str, joueur: str) -> Room:
        """L'hôte clôt la partie — la room survit le temps du feedback."""
        room = self.room(code)
        _verifier_hote(room, joueur)
        room.terminee = True
        return room

    def _en_manche(self, code: str) -> Room:
        room = self.room(code)
        if room.manche is None:
            raise ErreurRoom("pas_de_manche", "aucune manche en cours")
        return room

    def room(self, code: str) -> Room:
        """La room vivante — au passage, on purge les endormies et on touche celle-ci."""
        self._purger()
        room = self._rooms.get(code)
        if room is None:
            raise ErreurRoom("code_inconnu", f"code inconnu : {code}")
        room.activite = self._horloge()
        return room

    def _purger(self) -> None:
        """Une room que plus personne ne touche depuis 2 h n'a plus lieu d'être."""
        limite = self._horloge() - INACTIVITE
        for code, room in list(self._rooms.items()):
            if room.activite <= limite:
                del self._rooms[code]

    def _code_libre(self) -> str:
        while True:
            code = self._generer_code()
            if code not in self._rooms:
                return code


def _verifier_partie_ouverte(room: Room) -> None:
    if room.terminee:
        raise ErreurRoom("partie_terminee", "la partie est terminée")


def _verifier_hote(room: Room, joueur: str) -> None:
    if joueur != room.hote:
        raise ErreurRoom("pas_hote", "réservé à l'hôte")


def _pseudo_valide(pseudo: str) -> str:
    pseudo = pseudo.strip()
    if len(pseudo) < PSEUDO_MINIMUM:
        raise ErreurRoom(
            "pseudo_invalide", f"pseudo trop court ({PSEUDO_MINIMUM} caractères minimum)"
        )
    return pseudo


def _code_aleatoire() -> str:
    return "".join(random.choices(ALPHABET, k=LONGUEUR_CODE))
