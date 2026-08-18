from pathlib import Path

import pytest


@pytest.fixture
def chemin_contrat() -> Path:
    """Le contrat figé du repo — source de vérité des tests."""
    return Path(__file__).resolve().parents[2] / "fabrication" / "paires.json"
