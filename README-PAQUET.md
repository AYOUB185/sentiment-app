# sentiment-app

Classifieur de sentiment d'avis clients en français.

## Installation

```bash
pip install sentiment_app-1.0.0-py3-none-any.whl
```

## Utilisation en Python

```python
from sentiment_app import predict

resultat = predict("Livraison rapide, produit conforme, très satisfait")
print(resultat)  # {'label': 'positive', 'score': 0.7773}
```

## Utilisation en ligne de commande

```bash
# Résultat lisible
sentiment "Livraison rapide, produit conforme, très satisfait"
# → positive (confiance 78%)

# Résultat JSON
sentiment --json "Produit cassé et service injoignable"
# → {"label": "negative", "score": 0.7465}

# Version
sentiment --version
# → sentiment 1.0.0
```

## Fonctionnement

Le paquet embarque un modèle TF-IDF + Régression logistique entraîné sur des avis clients
en français. Il classe un avis comme `positive` ou `negative`.

Le modèle retourne un score de confiance entre 0 et 1. Un score faible (< 0,60) indique
que le modèle hésite ; dans ce cas, l'API expose le label `INDETERMINE`.

## Limites connues

- Le modèle a été entraîné sur un jeu de démonstration de 290 avis ; ses performances
  sur des domaines très différents (médical, juridique…) peuvent être réduites.
- Les avis très courts (un mot) ou hors-vocabulaire donnent souvent un score faible.
- L'ironie et les tournures négatives complexes peuvent tromper le modèle (sac de mots).
- La version de scikit-learn est figée à `1.5.*` pour garantir la compatibilité du modèle
  sérialisé.
