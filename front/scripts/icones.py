"""Les icônes de la PWA, sans dépendance : deux disques, un fond, un PNG.

    python scripts/icones.py

Regénère `public/icone-192.png` et `public/icone-512.png`.
"""

import struct
import zlib
from pathlib import Path

FOND = (0x12, 0x13, 0x1A)
PLEIN = (0xE8, 0xB0, 0x4B)
ANNEAU = (0x7F, 0xD1, 0xC1)
RAYON = 0.22
EPAISSEUR = 0.035
CENTRES = ((0.40, 0.5), (0.60, 0.5))
ECHANTILLONS = 3


def couleur(x: float, y: float) -> tuple[int, int, int]:
    """Le duo : un disque plein, un anneau — l'un ne dit rien de l'autre."""
    if _distance(x, y, CENTRES[0]) <= RAYON:
        return PLEIN
    if abs(_distance(x, y, CENTRES[1]) - RAYON) <= EPAISSEUR / 2:
        return ANNEAU
    return FOND


def _distance(x: float, y: float, centre: tuple[float, float]) -> float:
    return ((x - centre[0]) ** 2 + (y - centre[1]) ** 2) ** 0.5


def pixels(taille: int) -> bytes:
    lignes = bytearray()
    pas = 1 / (taille * ECHANTILLONS)
    for ligne in range(taille):
        lignes.append(0)
        for colonne in range(taille):
            total = [0, 0, 0]
            for sous_y in range(ECHANTILLONS):
                for sous_x in range(ECHANTILLONS):
                    teinte = couleur(
                        (colonne * ECHANTILLONS + sous_x + 0.5) * pas,
                        (ligne * ECHANTILLONS + sous_y + 0.5) * pas,
                    )
                    for canal in range(3):
                        total[canal] += teinte[canal]
            lignes.extend(canal // ECHANTILLONS**2 for canal in total)
    return bytes(lignes)


def png(taille: int) -> bytes:
    entete = struct.pack(">IIBBBBB", taille, taille, 8, 2, 0, 0, 0)
    return b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            _bloc(b"IHDR", entete),
            _bloc(b"IDAT", zlib.compress(pixels(taille), 9)),
            _bloc(b"IEND", b""),
        ]
    )


def _bloc(nom: bytes, donnees: bytes) -> bytes:
    return (
        struct.pack(">I", len(donnees))
        + nom
        + donnees
        + struct.pack(">I", zlib.crc32(nom + donnees) & 0xFFFFFFFF)
    )


if __name__ == "__main__":
    public = Path(__file__).resolve().parents[1] / "public"
    for taille in (192, 512):
        (public / f"icone-{taille}.png").write_bytes(png(taille))
