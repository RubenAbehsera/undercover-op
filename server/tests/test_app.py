import asyncio

import httpx
import pytest

from jeu.__main__ import main
from jeu.app import creer_app
from jeu.contrat import ErreurContrat


def test_le_serveur_demarre_avec_le_contrat(chemin_contrat):
    app = creer_app(chemin_contrat)

    reponse = asyncio.run(_appeler(app, "/sante"))

    assert reponse.status_code == 200
    assert reponse.json() == {"etat": "ok"}


def test_le_serveur_refuse_de_demarrer_sans_contrat(tmp_path):
    with pytest.raises(ErreurContrat, match="introuvable"):
        creer_app(tmp_path / "rien.json")


def test_le_process_plante_proprement_sans_contrat(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("CONTRAT_PAIRES", str(tmp_path / "rien.json"))

    with pytest.raises(SystemExit) as excinfo:
        main()

    assert excinfo.value.code == 1
    assert "introuvable" in capsys.readouterr().err


async def _appeler(app, chemin: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.get(chemin)
