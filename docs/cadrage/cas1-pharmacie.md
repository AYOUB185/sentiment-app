# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Repérer les champs obligatoires manquants ou incohérents sur une ordonnance avant sa validation par le pharmacien.

## Utilisateur final (obligatoire)

Le pharmacien et le préparateur en pharmacie utilisent le contrôle comme une aide à la vérification. Le pharmacien reste responsable de la validation finale de l'ordonnance.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(b) Les champs obligatoires et leurs règles peuvent être vérifiés directement à partir des exigences applicables, ce qui rend chaque alerte explicable. (a) Il n'est pas nécessaire de disposer d'un grand jeu d'ordonnances étiquetées pour appliquer des contrôles déterministes. (d) Une ordonnance déclarée complète à tort peut avoir une conséquence importante : le pharmacien doit donc contrôler toute alerte et garder la décision finale.

## Données nécessaires et leur origine (obligatoire)

Les champs de l'ordonnance (identité requise, date, prescripteur, médicament, dosage et signature selon le cas) proviennent du document présenté. Les règles de contrôle sont établies et validées à partir des textes applicables et des procédures internes de la pharmacie.

## Métrique de succès et seuil d'acceptation (obligatoire)

Mesurer le rappel des champs manquants sur un jeu d'ordonnances anonymisées et vérifiées par des pharmaciens ; viser au moins 99 % de champs manquants détectés. Mesurer aussi les fausses alertes et faire valider le seuil par le pharmacien avant la mise en service.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un champ manquant non signalé peut conduire à une validation inappropriée, tandis qu'une fausse alerte ralentit la délivrance. Le système signale les points à vérifier, mais aucun refus ni aucune validation définitive ne sont automatiques : le pharmacien tranche.

## Risques éthiques ou de confidentialité (obligatoire)

Une ordonnance contient des données de santé et des données personnelles. L'accès doit être réservé au personnel autorisé, les données de test doivent être anonymisées et les documents ne doivent pas être transmis à un service tiers non autorisé.

## Approche écartée et pourquoi (facultatif)

Le modèle génératif seul est écarté, car il pourrait inventer une règle ou manquer un champ obligatoire. Des règles explicites sont plus faciles à vérifier et à auditer pour ce contrôle.
