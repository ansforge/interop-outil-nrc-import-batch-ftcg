# Outil d'import en batch des traductions du FTCG

## À propos du projet
Ce projet a pour objectif d'extraire les traductions du FTCG (*French Translation Collaboration Group*) et de les comparer avec le contenu actuel de l'édition nationale française pour créer un fichier d'import batch utilisable dans l'Authoring Platform.
Le processus est le suivant :
- Lecture de la Common French
    - Extraire les synonymes (termes préférés et synonymes acceptables) actifs d'intérêt de la Common French
    - Exclure les concepts des hiérarchies 'Environnement ou lieu géographique' et 'Organisme'
- Lecture de l'édition nationale FR
    - Extraire les SCTIDs de concepts ayant des descriptions actives ou inactives françaises publiés
    - Ajouter les SCTIDs de concepts ayant des descriptions active ou inactives françaises non publiées via l'onglet "*Language Refset Details*" du rapport "*New and change components*" de l'Authoring Platform
- Conserver seulement les descriptions de la Common French associées à des concepts non traduits dans l'édition nationale
- Appliquer des contrôles qualité sur la casse et les règles éditoriales pour faciliter le travail de relecture

## Prérequis
Ce projet nécessite :
- un accès à l'Authoring Platform de la SNOMED Internationale
- un accès à serveur FHIR contenant la version de l'édition nationale dont dépend votre édition nationale non publiée

## Installation du projet
```shell
# Exemple avec le gestionnaire d'environnement venv
python3 -m venv ~/.venv/mon_env
source ~/.venv/mon_env/bin/activate

# Récupérer le projet
git clone git@github.com:ansforge/interop-outil-nrc-import-batch-ftcg.git
cd ./interop-outil-nrc-import-batch-ftcg/
pip install .
```

## Récupérer les modifications non publiées de votre édition nationale
- Connectez-vous à votre Authoring Platform
- Allez dans la section Reporting Platform
- Sélectionnez le rapport New and changed components
- Sélectionnez le projet d'intérêt
- Lancez le rapport sans paramètre
- Allez dans l'onglet Language Refset Details
- Téléchargez au format TSV

## Utilisation du projet
Le projet nécessite plusieurs données en entrée :
- La Snapshot d'une release de la Common French
- La date de la release de la Common French
- Le fichier description FR de la dernière release de l'édition nationale
- Le fichier TSV extrait de l'Authoring Platform
- L'endpoint de votre serveur FHIR

Utilisez la commande suivante pour générer le fichier d'import batch :
```shell
./import_batch_ftcg/main.py "/chemin_vers_Common_French/Snapshot/" "YYYYMMDD" "/chemin_vers_fichier_descriptions_fr" "chemin_vers_extrait_du_rapport" "chemin_vers_fichier_import_batch.tsv"  "endpoint_FTS" "chemin_vers_fichier_de_sortie.csv"
```

## Licence
Sous licence MIT, voir le fichier `LICENSE` pour plus d'informations.

## Remerciements
* https://github.com/eHealth-Suisse/SNOMED_Applications