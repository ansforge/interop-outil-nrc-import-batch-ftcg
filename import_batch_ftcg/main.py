#!/usr/bin/env python3

from import_batch_ftcg import io
from import_batch_ftcg import control
from import_batch_ftcg import server
import argparse

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("cf_path", type=str,
                     help="Chemin vers le dossier Snapshot de la Common French")
    cli.add_argument("cf_date", type=str, help="Date de release de la Common French")
    cli.add_argument("fr_path", type=str,
                     help="Chemin vers l'extrait du rapport New and change components")
    cli.add_argument("fr_date", type=str, help="Date de release de l'édition nationale")
    cli.add_argument("endpoint", type=str,
                     help="Endpoint du FTS contenant l'édition internationale dont \
                        dépend l'édition nationale non publiée")
    cli.add_argument("output", type=str, help="Emplacement et nom du fichier de sortie")
    args = cli.parse_args()

    # Initialisation de la classe de gestion du FTS
    fts = server.Fts(args.endpoint)
    # Lecture et pré-processus de la Common French
    cf = io.read_common_french(args.cf_path, args.cf_date, fts)
    print(f"\nCommon French extraite : {len(cf)} lignes.")
    # Lecture et pré-processus de l'édition nationale
    fr = io.get_fr_edition(args.fr_path, args.fr_date, args.unpub_fr_path)
    print(f"Edition nationale extraite : {len(fr)} lignes.")

    # Conserve seulement les traductions de la Common French pour des concepts dans
    # l'édition nationale n'ayant pas de description FR (active ou inactive)
    cf = cf.loc[~cf.loc[:, "conceptId"].isin(fr.loc[:, "conceptId"])]
    print(f"Réduction de la Common French à importer : {len(cf)} lignes d'intérêt.")

    # Vérification des règles pour relecture
    print("\nVérification du respect des règles éditoriales en cours...")
    cf = control.run_quality_control(cf)
    print("Vérification terminée")

    # Ecriture du fichier d'import
    io.write_batch_file(cf, args.output)
    print(f"\nFichier final sauvegardé : {args.output}")
