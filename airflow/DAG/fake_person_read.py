"""
Ce DAG va permettre d'extraire des données depuis une page WEB, de les transformer puis de les stocker au bon endroit dans le stockage local avant de faire des tests de BDD
"""

# Import des librairies nécessaires
from airflow.decorators import dag, task
import pendulum
import pymongo
import pandas as pd


@dag(schedule="@once", start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), catchup=False, tags=["fake_read"])
def fake_person_read():

    @task()
    def extract(path: str) -> list:
        """
        Tâche d'extraction de l'équipe souhaitée
        """

        df = pd.read_csv("path")

        return df

    @task()
    def transform(df_persons: pd.DataFrame):

        df_persons.drop(columns="Nom complet", axis=1)
        df_persons["Poids (g)"] = df_persons["Poids (kg)"] * 1000
        df_persons["Taille (m)"] = df_persons["Taille (cm)"] / 100
        df_persons.drop(columns=["Poids (kg)", "Taille (cm)"], axis=1, inplace=True)

        return df_persons

    @task()
    def connect_and_insert(transformed_df: pd.DataFrame):

        mongo_uri = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(mongo_uri)

        # Sélection de la base de données et de la collection
        db = client["test_db"]
        collection = db["fake_person"]

        # Insertion des données dans MongoDB
        collection.insert_many(transformed_df.to_dict(orient="records"))

        # Fermeture de la connexion
        client.close()

    df_persons = extract(path="airflow/data/data.csv")
    connect_and_insert(transform(df_persons))


# Lancement global de la fonction
fake_person_read()
