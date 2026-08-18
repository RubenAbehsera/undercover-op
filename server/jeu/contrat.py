"""Le contrat figé fabrication → jeu : chargement et validation.

Le serveur ne connaît du domaine One Piece que ce qui passe par ici
(``fabrication/paires.json``, ADR 0001 — pas de graphe en production).
"""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ValidationError

Difficulte = Literal["facile", "intermediaire"]


class ErreurContrat(Exception):
    """Le contrat est absent ou invalide — le serveur refuse de démarrer."""


class Personnage(BaseModel):
    id: str
    nom: str
    arc_premiere_apparition: str
    notoriete: int


class Lien(BaseModel):
    type: str
    libelle: str


class Paire(BaseModel):
    id: str
    majorite: str
    imposteur: str
    lien: Lien
    difficulte: Difficulte
    arc_etablissement: str


class Contrat(BaseModel):
    arcs: list[str]
    personnages: list[Personnage]
    paires: list[Paire]


def charger_contrat(chemin: Path) -> Contrat:
    try:
        contenu = chemin.read_text(encoding="utf-8")
    except FileNotFoundError as err:
        raise ErreurContrat(f"contrat introuvable : {chemin}") from err
    try:
        contrat = Contrat.model_validate_json(contenu)
    except ValidationError as err:
        raise ErreurContrat(_formater(err)) from err
    _verifier_references(contrat)
    return contrat


def _formater(err: ValidationError) -> str:
    lignes = [
        f"contrat invalide : {_chemin_champ(e['loc'])} — {e['msg']}"
        for e in err.errors()
    ]
    return "\n".join(lignes)


def _chemin_champ(loc: tuple) -> str:
    """Localisation pydantic en chemin lisible : paires[3].difficulte."""
    return "".join(
        f"[{maillon}]" if isinstance(maillon, int) else f".{maillon}"
        for maillon in loc
    ).lstrip(".")


def _verifier_references(contrat: Contrat) -> None:
    """Chaque personnage et chaque arc cités doivent exister dans le contrat."""
    ids = {p.id for p in contrat.personnages}
    arcs = set(contrat.arcs)
    for i, paire in enumerate(contrat.paires):
        for champ, valeur in (
            ("majorite", paire.majorite),
            ("imposteur", paire.imposteur),
        ):
            if valeur not in ids:
                raise _inconnu(f"paires[{i}].{champ}", "personnage", valeur)
        if paire.arc_etablissement not in arcs:
            raise _inconnu(f"paires[{i}].arc_etablissement", "arc", paire.arc_etablissement)
    for i, personnage in enumerate(contrat.personnages):
        if personnage.arc_premiere_apparition not in arcs:
            raise _inconnu(
                f"personnages[{i}].arc_premiere_apparition",
                "arc",
                personnage.arc_premiere_apparition,
            )


def _inconnu(chemin_champ: str, genre: str, valeur: str) -> ErreurContrat:
    return ErreurContrat(
        f"contrat invalide : {chemin_champ} — {genre} inconnu « {valeur} »"
    )
