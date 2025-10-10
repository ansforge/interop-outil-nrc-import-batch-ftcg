#!/usr/bin/env python3

import argparse

from import_batch_ftcg import control, io, server

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("cf_path", type=str,
                     help="Chemin vers le dossier Snapshot de la Common French")
    cli.add_argument("cf_date", type=str, help="Date de release de la Common French")
    cli.add_argument("fr_path", type=str, help="Chemin vers le fichier de descriptions \
                     FR de l'édition nationale")
    cli.add_argument("unpub_fr_path", type=str,
                     help="Chemin vers l'extrait du rapport New and change components")
    cli.add_argument("endpoint", type=str,
                     help="Endpoint du FTS contenant l'édition internationale dont \
                        dépend l'édition nationale non publiée")
    cli.add_argument("output", type=str, help="Emplacement et nom du fichier de sortie")
    args = cli.parse_args()

    # Initialisation de la classe de gestion du FTS
    fts = server.Fts(args.endpoint)
    # Lecture et pré-processus de la Common French
    print("\nExtraction Common French...", end="\r")
    cf = io.read_common_french(args.cf_path, args.cf_date, fts)
    print(f"Extraction Common French ({len(cf)} lignes) - OK")
    # Lecture et pré-processus de l'édition nationale
    print("Extraction édition nationale...", end="\r")
    fr = io.get_fr_edition(args.fr_path, args.unpub_fr_path)
    print(f"Extraction édition nationale ({len(fr)} SCTID) - OK")

    # Conserve seulement les traductions de la Common French pour des concepts dans
    # l'édition nationale n'ayant pas de description FR (active ou inactive)
    cf = cf.loc[~cf.loc[:, "conceptId"].isin(fr)]
    print(f"\nRéduction de la Common French à importer ({len(cf)} lignes) - OK")

    # Vérification des règles pour relecture
    print("\nVérification du respect des règles éditoriales...", end="\r")
    cf = control.run_quality_control(cf, fts)
    print("Vérification du respect des règles éditoriales - OK")

    # Ecriture du fichier d'import
    print("\nSauvegarde du fichier d'import...", end="\r")
    io.write_batch_file(cf, args.output)
    print(f"Sauvegarde du fichier d'import ({args.output}) - OK")
