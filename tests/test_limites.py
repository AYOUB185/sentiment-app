"""Tests aux limites du contrat d'entrée (TP4, étape B).

PredictRequest promet un champ « text », chaîne de 1 à 2000 caractères.
Ce fichier vérifie cette promesse à ses frontières, puis au hasard (hypothesis).
"""
import json
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")

LABELS_VALIDES = {"POSITIVE", "NEGATIVE", "INDETERMINE"}


@pytest.fixture(scope="module")
def client():
    """Portée « module » : l'API démarre une fois pour tout le fichier (hypothesis l'exige)."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:  # le « with » exécute le lifespan : le modèle est chargé
        yield c


def en_json(valeur: object) -> bytes:
    """Corps de requête JSON, sous forme d'octets : permet aussi d'envoyer un corps invalide."""
    if isinstance(valeur, bytes):
        return valeur
    return json.dumps(valeur).encode("utf-8")


# Étape B.1 : huit cas au moins, chacun avec son code attendu.
CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   "}), 422, id="texte-espaces"),
    pytest.param(en_json({"text": "a"}), 200, id="un-seul-caractere"),
    pytest.param(en_json({"text": "a" * 2000}), 200, id="exactement-2000-caracteres"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
    pytest.param(en_json({}), 422, id="champ-absent"),
    pytest.param(en_json({"text": 42}), 422, id="champ-type-invalide"),
    pytest.param(b"pas du json", 422, id="corps-non-json"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = client.post("/predict", content=corps, headers={"Content-Type": "application/json"})
    assert reponse.status_code == code_attendu
    # Étape B.2 : pour chaque 422, vérifiez aussi la FORME de la réponse :
    if code_attendu == 422:
        detail = reponse.json().get("detail")
        assert isinstance(detail, list), f"detail doit être une liste standard d'erreurs, obtenu : {detail!r}"
        assert len(detail) > 0
        for err in detail:
            assert isinstance(err, dict)
            assert "loc" in err
            assert "msg" in err
            assert "type" in err


# Étape B.5 : deux tests de propriété avec hypothesis.
@settings(deadline=None, max_examples=50)
@given(
    texte=st.text(min_size=1, max_size=2000).filter(lambda s: s.strip() != "")
)
def test_propriete_texte_valide_repond_200(client, texte):
    """Tout texte de 1 à 2000 caractères non vide après strip reçoit 200."""
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 200
    corps = reponse.json()
    assert corps["label"] in LABELS_VALIDES
    assert 0.0 <= corps["score"] <= 1.0
    assert "text" in corps


@settings(deadline=None, max_examples=50)
@given(
    texte=st.text(alphabet=" \t\r\n", min_size=1, max_size=50)
)
def test_propriete_blancs_seuls_refuses_422(client, texte):
    """Tout texte composé uniquement d'espaces reçoit 422 avec detail en liste."""
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 422
    detail = reponse.json().get("detail")
    assert isinstance(detail, list), f"detail doit être une liste standard d'erreurs, obtenu : {detail!r}"
