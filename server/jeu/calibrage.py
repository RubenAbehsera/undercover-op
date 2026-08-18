"""Le calibrage d'une room : jusqu'où l'histoire est connue des joueurs.

L'arc retenu est la borne maximale inclusive de l'anti-spoil. Une paire n'est
servable que si son lien *et* les deux personnages tiennent sous cette borne.
"""

from jeu.contrat import Contrat, Paire


def arcs_proposes(contrat: Contrat) -> list[str]:
    """Les calibrages qui changent réellement le pool, dans l'ordre canonique.

    Deux arcs consécutifs qui ouvrent les mêmes paires ne valent qu'un choix :
    on ne garde que celui qui en ouvre une de plus.
    """
    return [contrat.arcs[i] for i in sorted(set(_bornes(contrat).values()))]


def pool(contrat: Contrat, calibrage: str) -> list[Paire]:
    """Les paires servables sous ce calibrage, dans l'ordre du contrat."""
    borne = contrat.arcs.index(calibrage)
    bornes = _bornes(contrat)
    return [paire for paire in contrat.paires if bornes[paire.id] <= borne]


def _bornes(contrat: Contrat) -> dict[str, int]:
    """Par paire, le premier arc qui la rend servable : lien et duo réunis."""
    rang = {arc: i for i, arc in enumerate(contrat.arcs)}
    apparition = {p.id: rang[p.arc_premiere_apparition] for p in contrat.personnages}
    return {
        paire.id: max(
            rang[paire.arc_etablissement],
            apparition[paire.majorite],
            apparition[paire.imposteur],
        )
        for paire in contrat.paires
    }
