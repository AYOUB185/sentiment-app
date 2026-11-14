"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de src/predict.py, qui charge models/sentiment.joblib une seule fois.
"""
import sys
from pathlib import Path
from typing import Literal, TypedDict

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
from predict import charger_modele, predict as _predict  # noqa: E402, I001

Label = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
SEUIL_ABSTENTION: float = 0.60

CORRESPONDANCE_LABELS: dict[str, Label] = {
    "positive": "POSITIVE",
    "negative": "NEGATIVE",
}


class PredictionDict(TypedDict):
    label: Label
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        pipeline = charger_modele()  # échoue immédiatement si le joblib manque
        classes = getattr(pipeline, "classes_", None)
        if classes is not None:
            for c in classes:
                if str(c) not in CORRESPONDANCE_LABELS:
                    raise ValueError(
                        f"Classe inattendue dans le modèle : {c!r} "
                        f"(attendues : {list(CORRESPONDANCE_LABELS.keys())})"
                    )

    def predict(self, text: str) -> PredictionDict:
        """Renvoie {'label': 'POSITIVE'|'NEGATIVE'|'INDETERMINE', 'score': float, 'text': aperçu}."""
        r = _predict(text)  # lève ValueError si le texte est vide
        score = float(r["score"])
        brut = str(r["label"]).lower()

        if score < SEUIL_ABSTENTION:
            label: Label = "INDETERMINE"
        else:
            label = CORRESPONDANCE_LABELS.get(brut, "INDETERMINE")

        return {"label": label, "score": score, "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans src/predict.py)."""
    return SentimentClassifier()
