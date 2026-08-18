"""La mesure, persistée : un fichier SQLite, la stdlib, pas d'ORM.

Deux traces et deux seulement. Une par manche terminée — ce que la partie a
produit, sans jamais dire qui a joué quoi : la répartition des votes n'est
qu'une suite d'effectifs décroissants, l'identité des votants reste dans la
mémoire du serveur et meurt avec la room. Une par joueur et par partie — son
retour de fin, en trois niveaux (1 mauvais, 2 correct, 3 excellent).

Le drapeau « je ne connais pas » n'a pas de trace nominative : seul son
décompte survit, et il suffit — une manche qui en porte un est écartée du
calcul de qualité des tirages.
"""

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from jeu.erreurs import ErreurRoom

NIVEAUX = (1, 2, 3)

SCHEMA = """
CREATE TABLE IF NOT EXISTS manche (
    id INTEGER PRIMARY KEY,
    horodatage TEXT NOT NULL DEFAULT (datetime('now')),
    partie TEXT NOT NULL,
    calibrage TEXT NOT NULL,
    paire TEXT NOT NULL,
    joueurs INTEGER NOT NULL,
    tours INTEGER NOT NULL,
    demasque INTEGER NOT NULL,
    suffrages INTEGER NOT NULL,
    voix_imposteur INTEGER NOT NULL,
    repartition TEXT NOT NULL,
    drapeaux INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS retour (
    partie TEXT NOT NULL,
    joueur TEXT NOT NULL,
    horodatage TEXT NOT NULL DEFAULT (datetime('now')),
    niveau INTEGER NOT NULL,
    commentaire TEXT,
    PRIMARY KEY (partie, joueur)
);
"""


@dataclass(frozen=True)
class SignalManche:
    """Le signal objectif d'une manche, tel qu'il part en base."""

    partie: str
    calibrage: str
    paire: str
    joueurs: int
    tours: int
    demasque: bool
    suffrages: int
    voix_imposteur: int
    repartition: list[int]
    drapeaux: int


class Signaux:
    """Le magasin des signaux — un fichier, deux tables, des écritures unitaires."""

    def __init__(self, chemin: str | Path = ":memory:"):
        self._base = sqlite3.connect(chemin, check_same_thread=False)
        self._base.row_factory = sqlite3.Row
        self._base.executescript(SCHEMA)
        self._base.commit()

    def enregistrer_manche(self, signal: SignalManche) -> None:
        """La révélation passée, la manche laisse sa ligne."""
        self._base.execute(
            """
            INSERT INTO manche (
                partie, calibrage, paire, joueurs, tours, demasque,
                suffrages, voix_imposteur, repartition, drapeaux
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                signal.partie,
                signal.calibrage,
                signal.paire,
                signal.joueurs,
                signal.tours,
                int(signal.demasque),
                signal.suffrages,
                signal.voix_imposteur,
                json.dumps(signal.repartition),
                signal.drapeaux,
            ),
        )
        self._base.commit()

    def enregistrer_retour(
        self, partie: str, joueur: str, niveau: int, commentaire: str | None
    ) -> None:
        """Le retour subjectif d'un joueur : un seul par partie, définitif."""
        if niveau not in NIVEAUX:
            raise ErreurRoom("niveau_invalide", f"niveau hors des trois : {niveau}")
        try:
            self._base.execute(
                "INSERT INTO retour (partie, joueur, niveau, commentaire)"
                " VALUES (?, ?, ?, ?)",
                (partie, joueur, niveau, commentaire),
            )
        except sqlite3.IntegrityError:
            raise ErreurRoom("deja_repondu", "vous avez déjà donné votre retour")
        self._base.commit()

    def manches(self) -> list[dict]:
        lignes = self._base.execute("SELECT * FROM manche ORDER BY id")
        return [
            {
                **dict(ligne),
                "demasque": bool(ligne["demasque"]),
                "repartition": json.loads(ligne["repartition"]),
            }
            for ligne in lignes
        ]

    def retours(self) -> list[dict]:
        lignes = self._base.execute(
            "SELECT partie, joueur, horodatage, niveau, commentaire FROM retour"
            " ORDER BY horodatage, joueur"
        )
        return [dict(ligne) for ligne in lignes]

    def qualite_tirages(self) -> list[dict]:
        """Par paire, ce que valent ses manches — les drapeautées mises à part.

        Une manche ratée par méconnaissance du personnage ne dit rien de la
        paire : elle est écartée, pas comptée comme un échec.
        """
        lignes = self._base.execute(
            """
            SELECT paire,
                   COUNT(*) AS manches,
                   SUM(demasque) AS demasquees,
                   AVG(tours) AS tours_moyens
            FROM manche
            WHERE drapeaux = 0
            GROUP BY paire
            ORDER BY paire
            """
        )
        return [dict(ligne) for ligne in lignes]

    def fermer(self) -> None:
        self._base.close()
