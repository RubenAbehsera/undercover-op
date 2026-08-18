"""La manche : le tirage anti-spoil et la distribution des rôles.

L'étalon du tirage est `paires_servables` (conftest), recalculé à la main
depuis `docs/decisions.md` — jamais la fonction que l'on teste.
"""

import pytest

from jeu.calibrage import arcs_proposes, pool
from jeu.contrat import charger_contrat
from jeu.manche import Manches

JOUEURS = ["j-1", "j-2", "j-3", "j-4"]


@pytest.fixture
def contrat(chemin_contrat):
    return charger_contrat(chemin_contrat)


def test_aucun_tirage_ne_depasse_le_calibrage(contrat, paires_servables):
    for arc in arcs_proposes(contrat):
        manches = Manches(contrat, arc)
        servables = paires_servables(contrat, arc)

        for _ in range(2 * len(servables) + 1):
            paire = manches.lancer(JOUEURS).paire
            assert paire.id in servables, f"{paire.id} servie sous {arc}"


def test_aucune_repetition_avant_epuisement(contrat):
    calibrage = arcs_proposes(contrat)[-1]
    manches = Manches(contrat, calibrage)
    stock = len(pool(contrat, calibrage))

    tirees = [manches.lancer(JOUEURS).paire.id for _ in range(stock)]

    assert len(set(tirees)) == stock


def test_le_stock_epuise_se_reutilise(contrat):
    calibrage = arcs_proposes(contrat)[-1]
    manches = Manches(contrat, calibrage)
    stock = len(pool(contrat, calibrage))

    tirees = [manches.lancer(JOUEURS).paire.id for _ in range(2 * stock)]

    assert sorted(tirees) == sorted(2 * [paire.id for paire in pool(contrat, calibrage)])


def test_un_calibrage_etroit_tourne_sur_son_maigre_stock(contrat):
    calibrage = arcs_proposes(contrat)[0]
    manches = Manches(contrat, calibrage)
    servables = {paire.id for paire in pool(contrat, calibrage)}

    tirees = {manches.lancer(JOUEURS).paire.id for _ in range(20)}

    assert tirees == servables


def test_deux_parties_ne_tirent_pas_la_meme_suite(contrat):
    calibrage = arcs_proposes(contrat)[-1]

    suites = {
        tuple(Manches(contrat, calibrage).lancer(JOUEURS).paire.id for _ in range(5))
        for _ in range(20)
    }

    assert len(suites) > 1


@pytest.fixture
def manches(contrat):
    return Manches(contrat, arcs_proposes(contrat)[-1])


def test_un_seul_joueur_recoit_le_personnage_imposteur(manches):
    for _ in range(50):
        manche = manches.lancer(JOUEURS)

        vus = [manche.personnage(joueur)["id"] for joueur in JOUEURS]

        assert vus.count(manche.paire.imposteur) == 1
        assert vus.count(manche.paire.majorite) == len(JOUEURS) - 1


def test_le_personnage_porte_le_nom_du_contrat(contrat, manches):
    noms = {personnage.id: personnage.nom for personnage in contrat.personnages}

    manche = manches.lancer(JOUEURS)

    for joueur in JOUEURS:
        vu = manche.personnage(joueur)
        assert vu["nom"] == noms[vu["id"]]


def test_l_imposteur_n_est_pas_toujours_le_meme_joueur(manches):
    porteurs = {manches.lancer(JOUEURS).imposteur for _ in range(50)}

    assert porteurs == set(JOUEURS)


def test_le_payload_a_la_meme_forme_pour_tous(manches):
    manche = manches.lancer(JOUEURS)

    formes = {tuple(sorted(manche.personnage(joueur))) for joueur in JOUEURS}

    assert formes == {("id", "nom")}


def test_le_payload_ne_laisse_fuir_ni_le_lien_ni_la_difficulte_ni_le_role(manches):
    for _ in range(50):
        manche = manches.lancer(JOUEURS)

        for joueur in JOUEURS:
            texte = repr(manche.personnage(joueur))
            assert manche.paire.lien.libelle not in texte
            assert manche.paire.lien.type not in texte
            assert manche.paire.difficulte not in texte
            assert manche.paire.id not in texte
            assert manche.imposteur not in texte
