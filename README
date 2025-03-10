# Outil d'import en batch des traductions du FTCG

## À propos du projet
Ce projet a pour objectif d'extraire les traductions du FTCG (French Translation Collaboration Group) et de les comparer avec le contenu actuel de l'édition nationale française pour créer un fichier d'import batch utilisable dans l'Authoring Platform.
Le processus est le suivant :
- Lecture de la Common French
    - Extraire les synonymes (termes préférés et synonymes acceptables) actifs d'intérêt de la Common French
    - Extraire les FSN et suffixes sémantiques associés aux concepts de ces synonymes
    - Exclure les concepts des hiérarchies 'Environnement ou lieu géographique' et 'organisme'
- Lecture de l'édition nationale FR
    - Extraire les synonymes (termes préférés et synonymes acceptables) actifs et inactifs publiés
    - Ajouter l'acceptabilité de chacun des synonymes
    - Appliquer les modifications non-publiées via un extrait du rapport 'New and change components' de l'Authoring Platform
- Conserver seulement les descriptions de la Common French associées à des concepts non traduits dans l'édition nationale
- Appliquer des contrôles qualité sur la casse et les règles éditoriales pour faciliter le travail de relecture

## Prérequis
Ce projet nécessite un accès à l'Authoring Platform de la SNOMED Internationale

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
- Téléchargez le rapport
- Sauvegardez l'onglet Language Refset Details au format CSV

## Utilisation du projet
Le projet nécessite plusieurs données en entrée :
- La Snapshot d'une release de la Common French
- La date de la release de la Common French
- La Snapshot de la dernière release de l'édition nationale
- La date de la dernière release de l'édition nationale
- L'extrait du rapport New and Changed components

Utilisez la commande suivante pour générer le fichier d'import batch :
```shell
./import_batch_ftcg/main.py "/chemin_vers_Common_French/Snapshot/" "YYYYMMDD" "/chemin_vers_édition_nationale/Snapshot/" "YYYY0621" "chemin_vers_extrait_du_rapport" "chemin_vers_fichier_import_batch.csv"
```

## Licence
Sous licence MIT, voir le fichier `LICENSE` pour plus d'informations.

## Remerciements
* https://github.com/eHealth-Suisse/SNOMED_Applications