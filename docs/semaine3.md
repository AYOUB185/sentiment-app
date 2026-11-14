# Semaine 3 : l'API, notes du binôme

> Deux questions, quelques phrases chacune. Répondez avec ce que vous avez observé, pas avec le cours.

## 1. Pourquoi l'API refuse-t-elle de démarrer sans `models/sentiment.joblib`, plutôt que de démarrer et de répondre 503 ?

L'API applique le principe du « Fail-Fast » au démarrage via le gestionnaire de cycle de vie `lifespan`. Démarrer le service alors que le modèle est absent masquerait une anomalie de configuration critique lors du déploiement. Échouer immédiatement au démarrage signale clairement aux outils d'orchestration (Docker, Kubernetes) ou à la CI que le composant essentiel est indisponible, évitant de router inutilement du trafic vers un service incapable de rendre le service attendu.

## 2. Un texte vide est refusé deux fois : par Pydantic, puis par `predict()`. Est-ce redondant ?

Non, ce n'est pas redondant, il s'agit d'une application du principe de défense en profondeur (Defense in Depth). La validation Pydantic (`PredictRequest`) protège l'interface HTTP et garantit un rejet précoce normalisé avec le code 422 au niveau de la couche web. La validation interne à `predict()` garantit quant à elle l'intégrité de la couche métier et de la fonction Python unitaire, qui peut être appelée indépendamment de FastAPI (en scripts batch, CLI, ou notebooks) sans dépendre du serveur web.
