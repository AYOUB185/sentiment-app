# Changelog — sentiment-app

Toutes les modifications notables de ce projet sont documentées ici.
Format : [Semantic Versioning](https://semver.org/lang/fr/).

## [1.0.0] - 2026-11-14

### Ajouté

- Paquet Python `sentiment_app` distribuable via wheel
- Fonction publique `predict(texte: str) -> Resultat` (label + score)
- Commande CLI `sentiment` avec options `--json` et `--version`
- Modèle TF-IDF + Régression logistique embarqué dans la roue (`modele/sentiment.joblib`)
- Chargement du modèle via `importlib.resources` (indépendant du chemin d'installation)
- Cache LRU sur `charger_modele()` pour éviter les rechargements inutiles

### Limites connues

- Entraîné sur jeu de démonstration (290 avis) — performances limitées hors-domaine
- Ironie et lexique ambigu non détectés (modèle sac de mots)
- scikit-learn figé à `1.5.*` pour compatibilité du modèle sérialisé

