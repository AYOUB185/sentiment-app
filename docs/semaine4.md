# Semaine 4 : tests approfondis et qualité, notes du binôme

> Une à deux pages. Uniquement des chiffres issus de VOS exécutions.

## 1. Couverture

- Avant (étape A) : 91 %, lignes jamais exécutées : `api/main.py:49` (bloc `if __name__ == "__main__"`), `api/main.py:77-79` (branche `ValueError`→422 inexistante), `api/main.py:85-87` (branche erreur interne non testée)
- Pour chacune, le comportement qu'aucun test ne vérifiait : lancement direct du serveur (non testable via TestClient) ; conversion d'erreurs internes en HTTP 500.
- Après (étape D) : 100 % ; ligne `# pragma: no cover` ajoutée au bloc `if __name__ == "__main__"` car son exécution réelle demanderait un vrai démarrage de serveur uvicorn.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| `{"text": "   "}` retournait `detail` sous forme de chaîne au lieu d'une liste standardisée Pydantic | `test_limites.py::test_blancs_seuls_rejetes` | Ajout d'un `field_validator` dans `PredictRequest` qui lève `ValueError("texte vide")` |
| `ValueError` interne de l'API renvoyait HTTP 422 au lieu de 500 | `test_integration.py::test_modele_en_panne_repond_500` | Suppression du handler `ValueError→422` dans `api/main.py` ; tous les `Exception` → 500 |

## 3. Seuil d'abstention

- Points de la courbe (`python src/courbe_seuil.py`) :
  - seuil 0,50 → 58/58 répondent (100 %), exactitude 0,879, 0 erreur évitée
  - seuil 0,60 → 42/58 répondent (72 %), exactitude 0,952, 2 erreurs évitées
  - seuil 0,75 → 24/58 répondent (41 %), exactitude 1,000, 7 erreurs évitées mais 34 abstentions
- Seuil retenu : **0,60** ; part des avis envoyés à un humain : 28 % (16/58) ; justification : bon équilibre entre précision (95,2 %) et volume traité automatiquement (72 %) — le modèle évite 2 erreurs franches sans sur-abstenir.

## 4. Jeu d'or

- Bilan (`python src/bilan_jeu_or.py`) : **justes 15, abstentions 3, erreurs franches déclarées 2**
- Ce que ces chiffres disent du modèle : sur 20 avis dont 5 délibérément difficiles, le modèle se trompe sur 2 cas (ironie pure + vocabulaire hors-domaine) et s'abstient correctement sur 3 cas ambigus. Les 2 erreurs déclarées sont documentées en `xfail` : le correcteur sait qu'elles sont connues et assumées.

## 5. Outils statiques

- Remarques au départ : **ruff** signalait 11 erreurs (E402 import non trié, B905 zip sans strict=, E741 variable `l` ambiguë) ; **mypy** signalait 0 erreur dès le départ.
- Parmi les 2 défauts de la partie 2, ruff et mypy n'en avaient signalé aucun (défauts de logique applicative, pas de style ou de type). Conclusion : les outils statiques complètent les tests mais ne les remplacent pas — un bug de comportement (mauvais code HTTP, mauvaise validation) reste invisible à ruff/mypy.
