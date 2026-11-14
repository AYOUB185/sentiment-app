"""Tests du paquet installé (TP Paquet).

Ces tests visent le paquet INSTALLÉ. Dans le dépôt, l'API ajoute src/ au chemin d'import :
sentiment_app y serait trouvé dans les sources, ce qui ne prouve rien. On les ignore donc,
sauf quand scripts/verifier_livrable.py les lance (VERIFICATION_LIVRABLE=1) : là, ils doivent
passer.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

_spec = importlib.util.find_spec("sentiment_app")
if (
    not (_spec and "site-packages" in (_spec.origin or ""))
    and not os.environ.get("VERIFICATION_LIVRABLE")
):
    import pytest

    pytest.skip(
        "paquet non installé : python scripts/verifier_livrable.py",
        allow_module_level=True,
    )

import sentiment_app  # noqa: E402

# La commande est installée à côté de l'interpréteur qui lance les tests.
COMMANDE = shutil.which("sentiment", path=str(Path(sys.executable).parent))

AVIS_POSITIF = "Livraison rapide, produit conforme, très satisfait"
AVIS_NEGATIF = "Produit cassé et service injoignable, à fuir"


def test_importe_depuis_le_paquet_installe():
    assert "site-packages" in sentiment_app.__file__, (
        "le test lit les sources, pas la roue installée"
    )


def test_version_disponible():
    assert isinstance(sentiment_app.__version__, str)
    assert sentiment_app.__version__ == "1.0.0"


def test_predict_positif():
    r = sentiment_app.predict(AVIS_POSITIF)
    assert r["label"] in ("positive", "negative")
    assert 0.0 <= r["score"] <= 1.0


def test_predict_negatif():
    r = sentiment_app.predict(AVIS_NEGATIF)
    assert r["label"] in ("positive", "negative")
    assert 0.0 <= r["score"] <= 1.0


def test_predict_texte_vide_leve_valueerror():
    import pytest as _pytest

    with _pytest.raises(ValueError, match="texte vide"):
        sentiment_app.predict("   ")


def test_commande_installee():
    assert COMMANDE is not None, "la commande 'sentiment' n'est pas installée"
    result = subprocess.run(
        [COMMANDE, "--json", AVIS_NEGATIF],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    import json

    data = json.loads(result.stdout)
    assert "label" in data
    assert "score" in data

