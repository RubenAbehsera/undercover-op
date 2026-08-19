"""Les icones de la PWA, sans dependance : un chapeau de paille, un ciel, un PNG.

    python scripts/icones.py

Regenere `public/icone-192.png` et `public/icone-512.png`.
"""

import struct
import zlib
from pathlib import Path

CIEL = (0x7C, 0xC6, 0xEA)
PAILLE = (0xF6, 0xDD, 0xA6)
PAILLE_BORD = (0xEB, 0xCB, 0x84)
LISERE = (0xA8, 0x7C, 0x2A)
RUBAN = (0xD6, 0x40, 0x2C)
ECHANTILLONS = 3

CALOTTE = (0.5, 0.615, 0.235, 0.305)  # centre x, y, demi-largeur, demi-hauteur
BORD = (0.5, 0.625, 0.445, 0.135)
RUBAN_HAUT, RUBAN_BAS = 0.505, 0.592


def couleur(x: float, y: float) -> tuple[int, int, int]:
    """Le chapeau de paille : une calotte, un ruban, un bord — sur le ciel."""
    if _dans(x, y, CALOTTE) <= 1 and y <= CALOTTE[1]:
        if _dans(x, y, CALOTTE) >= 0.86:
            return LISERE
        return RUBAN if RUBAN_HAUT <= y <= RUBAN_BAS else PAILLE
    rayon = _dans(x, y, BORD)
    if rayon <= 1:
        return LISERE if rayon >= 0.9 else PAILLE_BORD
    return CIEL


def _dans(x: float, y: float, ellipse: tuple[float, float, float, float]) -> float:
    """La distance normalisee au centre d'une ellipse : 1 sur son contour."""
    centre_x, centre_y, demi_x, demi_y = ellipse
    return ((x - centre_x) / demi_x) ** 2 + ((y - centre_y) / demi_y) ** 2


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
