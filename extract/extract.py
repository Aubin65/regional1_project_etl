"""
Cette partie est utilisée pour extraire la donnée depuis le site de la FFR
"""

import luigi

class ExtractJoueur(luigi.Task):
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

    def output(self):
        """
        Cette fonction renvoie une 
        """
        return luigi.LocalTarget("transformed_data.csv")

    def run(self):
        