from pathlib import Path

import pytest


@pytest.fixture
def chemin_contrat() -> Path:
    """Le contrat figé du repo — source de vérité des tests."""
    return Path(__file__).resolve().parents[2] / "fabrication" / "paires.json"


@pytest.fixture
def paires_servables():
    """Les paires servables sous un calibrage — définition de `docs/decisions.md`.

    Recalculée ici à la main, indépendamment de `jeu.calibrage` : c'est l'étalon
    contre lequel l'anti-spoil du serveur est vérifié.
    """

    def servables(contrat, calibrage: str) -> set[str]:
        rang = {arc: i for i, arc in enumerate(contrat.arcs)}
        apparition = {p.id: rang[p.arc_premiere_apparition] for p in contrat.personnages}
        borne = rang[calibrage]
        return {
            paire.id
            for paire in contrat.paires
            if rang[paire.arc_etablissement] <= borne
            and apparition[paire.majorite] <= borne
            and apparition[paire.imposteur] <= borne
        }

    return servables
