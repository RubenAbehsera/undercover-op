"""L'app ASGI du service de jeu : FastAPI pour le HTTP, socket.io pour le temps réel."""

import os
from pathlib import Path

import socketio
from fastapi import FastAPI

from jeu.contrat import Contrat, charger_contrat
from jeu.evenements import enregistrer
from jeu.rooms import Rooms
from jeu.signaux import Signaux


def creer_app(
    chemin_contrat: Path | None = None, chemin_signaux: str | Path | None = None
):
    """Fabrique l'app complète ; charge et valide le contrat au démarrage.

    Sans contrat valide, refuse de naître — jamais de serveur lancé sur un
    contrat bancal.
    """
    contrat = charger_contrat(chemin_contrat or _chemin_par_defaut())
    signaux = Signaux(chemin_signaux or _signaux_par_defaut())

    api = FastAPI(title="Undercover OP")
    api.state.contrat = contrat

    @api.get("/sante")
    def sante() -> dict:
        return {"etat": "ok"}

    sio = socketio.AsyncServer(async_mode="asgi")
    enregistrer(sio, Rooms(contrat, signaux=signaux))
    return socketio.ASGIApp(sio, other_asgi_app=api)


def _chemin_par_defaut() -> Path:
    variable = os.environ.get("CONTRAT_PAIRES")
    if variable:
        return Path(variable)
    return Path(__file__).resolve().parents[2] / "fabrication" / "paires.json"


def _signaux_par_defaut() -> Path:
    """Le fichier SQLite des signaux — sur le volume en production."""
    variable = os.environ.get("SIGNAUX_SQLITE")
    if variable:
        return Path(variable)
    return Path(__file__).resolve().parents[1] / "signaux.db"
