# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Répondre aux questions des élèves, parents et personnels sur le règlement intérieur en s'appuyant sur les passages officiels du document en vigueur.

## Utilisateur final (obligatoire)

Les élèves, les parents et les membres du personnel de l'école consultent l'assistant pour comprendre les règles, les procédures et les démarches. Le secrétariat ou la direction peut reprendre les questions complexes.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(b) La réponse doit pouvoir être vérifiée dans un article précis du règlement : le RAG peut retrouver le passage pertinent et le citer. (a) Il n'est pas indispensable de disposer dès le départ d'un grand jeu de questions-réponses étiquetées, car la source principale est le règlement existant. (d) Une réponse erronée sur une sanction, une absence ou un délai peut induire l'élève en erreur ; l'assistant doit donc s'abstenir lorsque le document ne permet pas de répondre et orienter vers le secrétariat.

## Données nécessaires et leur origine (obligatoire)

Le règlement intérieur officiel, ses annexes et les procédures validées par la direction sont les sources documentaires. Chaque document doit comporter sa date et sa version ; un petit ensemble de questions rédigées et validées par le personnel servira à tester les réponses.

## Métrique de succès et seuil d'acceptation (obligatoire)

Évaluer un jeu de questions tenu à l'écart : viser au moins 90 % de réponses jugées correctes par le personnel et 100 % de réponses accompagnées d'une référence au passage source. Toute réponse non étayée par le règlement doit être refusée ou transférée à un humain.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une réponse inexacte peut provoquer une mauvaise compréhension des droits, des obligations ou des délais. Les cas ambigus et les sujets disciplinaires sont transmis au secrétariat ou à la direction, qui confirme l'interprétation officielle.

## Risques éthiques ou de confidentialité (obligatoire)

Les questions peuvent révéler l'identité ou la situation personnelle d'un élève. Il faut limiter les informations collectées, contrôler les accès, protéger les journaux de conversation et éviter d'afficher des informations personnelles dans les réponses.

## Approche écartée et pourquoi (facultatif)

Un modèle génératif seul est écarté, car il pourrait produire une réponse plausible mais absente du règlement. Des règles métier seules ne couvriraient pas facilement toutes les formulations possibles des questions.
