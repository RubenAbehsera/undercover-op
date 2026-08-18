"""Les refus que le serveur sait expliquer.

Un motif court, stable, que le client peut afficher — jamais une trace Python.
"""


class ErreurRoom(Exception):
    """Une demande refusée, avec le motif que le client doit pouvoir afficher."""

    def __init__(self, motif: str, message: str):
        super().__init__(message)
        self.motif = motif
