"""
Cette partie est utilisée pour transformer le fichier créé par la partie extract de l'ETL Luigi
"""

from extract.code.extract import ExtractJoueur
import luigi
import json
import os


class TransformJoueur(luigi.Task):
    """Tâche permettant l'acquisition d'une équipe au format
    compositions = {
        nom_equipe_1: {
            "1" : Initiale. Nom,
            "2" : Initiale. Nom,
            ...
        }
        nom_equipe_2: {
            "1" : Initiale. Nom,
            "2" : Initiale. Nom,
            ...
        }
    }
    """

    def requires(self):
        return ExtractJoueur()

    def output(self):
        """
        Cette fonction enregistre les données extraites au format JSON de manière temporaire
        """
        return luigi.LocalTarget("luigi/transform/temp_storage/transformed_data.json")

    def run(self):
        """
        Cette fonction va venir ouvrir le fichier de stockage temporaire en json et y apporter les modifications nécessaires :
            - Passer les noms des joueurs en majuscules et enlever les espaces entre l'initiale et le nom
            - Passer les noms des clubs en minuscule
        """

        with self.input().open("r") as f:
            data = json.load(f)

        transformed_data = {
            team.lower(): {poste: joueur.upper().replace(" ", "") for poste, joueur in data[team].items()}
            for team in data
        }

        with self.output().open("w") as f:
            json.dump(transformed_data, f, indent=4)

    def on_success(self):
        os.remove("luigi/extract/temp_storage/extracted_data.json")
        print("---------------------------------------------")
        print(f"{self.input().path} removed successfully !")
        print("---------------------------------------------")
