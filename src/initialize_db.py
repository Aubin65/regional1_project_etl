"""
Ce fichier est utilisé pour l'initialisation de la base de données PostgreSQL dans le projet
"""

# Import des fonctions de base pour la réalisation de requêtes SQL
from psql_functions import connect_db, disconnect_db, execute_request  # noqa

conn, cursor = connect_db(name="test", user="test", pwd="test")

rows = execute_request()
