"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D).

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.main import app

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_de_demarrer(monkeypatch, tmp_path):
    """D.2 : Modèle absent : chemin redirigé, cache vidé, l'API refuse de démarrer."""
    import predict

    faux_chemin = tmp_path / "inexistant.joblib"
    monkeypatch.setattr(predict, "MODELE", faux_chemin)
    predict.charger_modele.cache_clear()

    try:
        with pytest.raises(FileNotFoundError, match="absent : lancez python src/train.py"):
            with TestClient(app):
                pass
    finally:
        predict.charger_modele.cache_clear()


def test_modele_non_charge_repond_503(monkeypatch):
    """D.3 : Modèle non chargé : modèle retiré de app.state, 503 sur /health et /predict."""
    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", None)
        r_health = client.get("/health")
        assert r_health.status_code == 503
        assert r_health.json()["detail"] == "Modèle non chargé"

        r_predict = client.post("/predict", json={"text": "Texte valide"})
        assert r_predict.status_code == 503
        assert r_predict.json()["detail"] == "Modèle non chargé"


@pytest.mark.parametrize("exception_levee", [
    RuntimeError("Panne moteur"),
    ValueError("bug interne de calcul"),
])
def test_modele_en_panne_repond_500(monkeypatch, exception_levee):
    """D.4 : Modèle en panne : predict lève une exception -> 500 sans fuite de message interne."""
    with TestClient(app) as client:
        mock_clf = MagicMock()
        mock_clf.predict.side_effect = exception_levee
        monkeypatch.setattr(app.state, "classifier", mock_clf)

        reponse = client.post("/predict", json={"text": "Texte valide pour test de panne"})
        assert reponse.status_code == 500
        corps = reponse.json()
        assert corps["detail"] == "Erreur interne du serveur"
        # Le message interne ne doit jamais fuiter côté client
        assert str(exception_levee) not in str(corps)


def test_classes_inattendues_refusees_au_demarrage(monkeypatch):
    """Étape E.3 : vérifie qu'un modèle avec des classes inconnues lève ValueError."""
    import api.model
    from api.model import SentimentClassifier

    mock_pipeline = MagicMock()
    mock_pipeline.classes_ = ["spam", "ham"]
    monkeypatch.setattr(api.model, "charger_modele", lambda: mock_pipeline)

    with pytest.raises(ValueError, match="Classe inattendue dans le modèle"):
        SentimentClassifier()

