"""
Ce fichier a pour but de définir les fonctions utiles à l'utilisation de PostgreSQL avec Python
"""

import psycopg2


def connect_db(
    name: str, user: str, pwd: str, host: str = "localhost", port: str = "5432"
) -> psycopg2.extensions.cursor:
    """Fonction de connexion à la base de données PostgreSQL

    Parameters
    ----------
    name : str
        nom de la base de données
    user : str
        utilisateur de la base de données
    pwd : str
        mot de passe associé à l'utilisateur de la base de données
    host : str, optional
        hôte de PostgreSQL, by default "localhost"
    port : str, optional
        port utilisé, by default "5432"

    Returns
    -------
    psycopg2.extensions.cursor
        curseur d'exécution des requêtes SQL
    """

    # Connexion à la base de données
    conn = psycopg2.connect(dbname=name, user=user, password=pwd, host=host, port=port)

    print(f"L'utilisateur : {user} est bien connecté à la base : {name}")

    # Création d'un curseur pour exécuter des commandes SQL
    cursor = conn.cursor()

    return conn, cursor


def disconnect_db(conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor) -> None:
    """Fonction de déconnexion à la base de données PostgreSQL

    Parameters
    ----------
    conn : psycopg2.extensions.connection
        connecteur à la base de données
    cursor : psycopg2.extensions.cursor
        curseur d'exécution des requêtes SQL
    """

    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()


def executer_request(request: str, cursor: psycopg2.extensions.cursor) -> list[tuple]:
    """Exécute une requête SQL

    Parameters
    ----------
    request : str
        contenu de la requête SQL
    cursor : psycopg2.extensions.cursor
        curseur d'exécution des requêtes SQL

    Returns
    -------
    list[tuple]
        résultat de la requête
    """

    try:
        # Exécution de la requête
        cursor.execute(request)

        # Récupération des lignes
        rows = cursor.fetchall()

        # Affichage des résultats
        for row in rows:
            print(row)

        return rows

    except psycopg2.Error as e:
        # Gestion des erreurs
        print(f"Une erreur s'est produite lors de l'exécution de la requête : {e}")
        return []  # Retourner une liste vide en cas d'erreur
