# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Classer automatiquement les avis clients d'un site e-commerce afin de faire remonter en priorité les avis négatifs à traiter par le service client.

## Utilisateur final (obligatoire)

Les agents du service client et les responsables de la qualité consultent la file priorisée pour repérer rapidement les clients insatisfaits. Ils vérifient le contenu de l'avis et décident de la réponse à apporter.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Les avis historiques peuvent être étiquetés positifs ou négatifs par les agents afin de constituer un jeu d'entraînement et de test. (c) Le site reçoit potentiellement des milliers d'avis : un classifieur entraîné permet de traiter chaque nouvel avis à faible coût. (d) Un avis négatif classé positif peut retarder une réclamation ; les résultats doivent donc être priorisés et contrôlés par un agent plutôt que déclencher automatiquement une décision commerciale.

## Données nécessaires et leur origine (obligatoire)

Les textes des avis, leur date et leur étiquette de sentiment proviennent de l'historique du site e-commerce et des corrections validées par les agents. Les données sont nettoyées et anonymisées avant l'entraînement, puis séparées en jeux d'entraînement, de validation et de test.

## Métrique de succès et seuil d'acceptation (obligatoire)

Mesurer le F1 macro sur un jeu de test indépendant et le rappel de la classe négative, qui est prioritaire pour ce besoin. Viser un F1 macro d'au moins 0,85 et un rappel des avis négatifs d'au moins 0,90 avant un déploiement assisté.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un avis négatif classé positif risque de ne pas être traité assez vite, tandis qu'un avis positif classé négatif augmente inutilement la charge des agents. Un agent vérifie les avis prioritaires, corrige le verdict si nécessaire et décide de la suite à donner au client.

## Risques éthiques ou de confidentialité (obligatoire)

Les avis peuvent contenir des noms, coordonnées ou informations sensibles. Il faut anonymiser ces éléments, limiter l'accès aux données et surveiller les erreurs selon les produits, les langues et les formulations afin d'éviter de défavoriser certains clients.

## Approche écartée et pourquoi (facultatif)

Des règles par mots-clés sont écartées comme approche principale, car une négation, l'ironie ou une formulation inhabituelle peuvent inverser le sens d'un avis. Elles peuvent néanmoins servir de contrôle complémentaire simple.
