"""Point d'entrée : ``python -m jeu``."""

import sys

import uvicorn

from jeu.app import creer_app
from jeu.contrat import ErreurContrat


def main() -> None:
    try:
        app = creer_app()
    except ErreurContrat as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
