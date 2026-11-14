# Semaine 5 : l'interface, notes du binôme

> Trois questions, quelques phrases chacune. Répondez avec ce que vous avez observé.

## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?

L'architecture du projet sépare clairement les responsabilités : `api/` charge et interroge le modèle, `ui/` ne fait qu'afficher des résultats reçus de l'API via HTTP. Si l'interface importait directement `predict()`, toute modification du modèle (changement de chemin, nouveau format de sortie) casserait l'interface. En passant par l'API, les deux couches évoluent indépendamment : le modèle peut être remplacé sans toucher l'interface, et l'interface peut tourner sur une machine différente du modèle.

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Quand le score de confiance est inférieur au seuil de 0,60, l'API renvoie `INDETERMINE` et l'interface affiche : *"La confiance est sous le seuil d'abstention : un humain doit trancher."* Un verdict forcé sur un cas douteux serait potentiellement faux, sans aucun signal pour l'utilisateur. Le mécanisme d'abstention préserve la confiance dans le système : l'utilisateur sait qu'il peut se fier aux verdicts POSITIVE/NEGATIVE affichés, et qu'un humain reste dans la boucle pour les cas ambigus.

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

Quand l'API est injoignable (serveur arrêté ou réseau coupé), l'interface affiche le message *"API injoignable : lancez d'abord uvicorn api.main:app"* — pas d'exception brute, pas de page blanche. Sur le fichier `data/avis_exemple.csv` (6 avis), l'analyse donne : 3 avis positifs (livraison rapide, emballage soigné, "Pas déçu"), 2 avis négatifs (produit cassé, commande jamais reçue), 1 indéterminé ("xqzvb wlkptr grombu"). **1 avis part vers un humain** (INDETERMINE).
