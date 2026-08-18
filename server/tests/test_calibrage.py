"""Le calibrage proposé à l'hôte : les arcs qui changent réellement le pool."""

from jeu.calibrage import arcs_proposes
from jeu.contrat import charger_contrat


def _pool(contrat, calibrage: str) -> set[str]:
    """Les paires servables sous ce calibrage — définition de `docs/decisions.md`."""
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


def test_les_arcs_proposes_suivent_l_ordre_canonique(chemin_contrat):
    contrat = charger_contrat(chemin_contrat)

    proposes = arcs_proposes(contrat)

    assert set(proposes) <= set(contrat.arcs)
    assert proposes == [arc for arc in contrat.arcs if arc in set(proposes)]


def test_chaque_arc_propose_agrandit_le_pool(chemin_contrat):
    contrat = charger_contrat(chemin_contrat)

    precedent: set[str] = set()
    for arc in arcs_proposes(contrat):
        pool = _pool(contrat, arc)
        assert pool > precedent, f"{arc} n'ajoute aucune paire"
        precedent = pool


def test_aucun_autre_arc_n_agrandit_le_pool(chemin_contrat):
    contrat = charger_contrat(chemin_contrat)
    proposes = arcs_proposes(contrat)

    dernier_propose = None
    for arc in contrat.arcs:
        if arc in proposes:
            dernier_propose = arc
            continue
        attendu = _pool(contrat, dernier_propose) if dernier_propose else set()
        assert _pool(contrat, arc) == attendu, f"{arc} change le pool sans être proposé"


def test_le_dernier_arc_propose_ouvre_tout_le_contrat(chemin_contrat):
    contrat = charger_contrat(chemin_contrat)

    assert _pool(contrat, arcs_proposes(contrat)[-1]) == {p.id for p in contrat.paires}
