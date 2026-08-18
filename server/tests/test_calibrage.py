"""Le calibrage proposé à l'hôte : les arcs qui changent réellement le pool."""

from jeu.calibrage import arcs_proposes, pool
from jeu.contrat import charger_contrat


def test_les_arcs_proposes_suivent_l_ordre_canonique(chemin_contrat, paires_servables):
    contrat = charger_contrat(chemin_contrat)

    proposes = arcs_proposes(contrat)

    assert set(proposes) <= set(contrat.arcs)
    assert proposes == [arc for arc in contrat.arcs if arc in set(proposes)]


def test_chaque_arc_propose_agrandit_le_pool(chemin_contrat, paires_servables):
    contrat = charger_contrat(chemin_contrat)

    precedent: set[str] = set()
    for arc in arcs_proposes(contrat):
        pool = paires_servables(contrat, arc)
        assert pool > precedent, f"{arc} n'ajoute aucune paire"
        precedent = pool


def test_aucun_autre_arc_n_agrandit_le_pool(chemin_contrat, paires_servables):
    contrat = charger_contrat(chemin_contrat)
    proposes = arcs_proposes(contrat)

    dernier_propose = None
    for arc in contrat.arcs:
        if arc in proposes:
            dernier_propose = arc
            continue
        attendu = paires_servables(contrat, dernier_propose) if dernier_propose else set()
        assert paires_servables(contrat, arc) == attendu, f"{arc} change le pool"


def test_le_dernier_arc_propose_ouvre_tout_le_contrat(chemin_contrat, paires_servables):
    contrat = charger_contrat(chemin_contrat)

    tout = {p.id for p in contrat.paires}

    assert paires_servables(contrat, arcs_proposes(contrat)[-1]) == tout


def test_le_pool_ne_sert_que_des_paires_sous_le_calibrage(chemin_contrat, paires_servables):
    contrat = charger_contrat(chemin_contrat)

    for arc in contrat.arcs:
        servables = {paire.id for paire in pool(contrat, arc)}
        assert servables == paires_servables(contrat, arc), f"pool faux pour {arc}"
