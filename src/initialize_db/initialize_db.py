"""
Ce fichier est utilisé pour l'initialisation de la base de données PostgreSQL dans le projet
"""

# Import des fonctions de base pour la réalisation de requêtes SQL
from psql_functions import connect_db, disconnect_db, execute_request
import os
from dotenv import load_dotenv

# Charger les variables de connexion
load_dotenv()

# Initialisation des paramètres de connexion à la base de données
db_name = os.environ.get("PSQL_DB_NAME")
user = os.environ.get("PSQL_USER")
pwd = os.environ.get("PSQL_PASSWORD")
host = os.environ.get("PSQL_HOST")
port = os.environ.get("PSQL_PORT")

# Connexion à la base de données
conn, cursor = connect_db(name=db_name, user=user, pwd=pwd, host=host, port=port)

# Initialisation de la liste des étapes d'initialisation de la base de données
steps = [
    "initialise_journee.sql",
    "initialise_equipe.sql",
    "initialise_match.sql",
    "initialise_carton.sql",
    "initialise_joueur.sql",
    "initialise_remplacement.sql",
    "initialise_historique_joueur.sql",
    "initialise_points.sql",
]

for step in steps:

    # Récupération de la requête
    with open(step, "r") as file:
        request = file.read()

    # Exécution de la requête
    execute_request(request=request, cursor=cursor)

# Déconnexion de la base de données
disconnect_db(conn=conn, cursor=cursor)
