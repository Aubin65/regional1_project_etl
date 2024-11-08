"""
Ce DAG va permettre d'extraire des données depuis une page WEB, de les transformer puis de les stocker au bon endroit dans le stockage local avant de faire des tests de BDD
"""

# Import des librairies nécessaires
from airflow.decorators import dag, task
import pendulum
import pymongo
from faker import Faker
import random


@dag(schedule="@once", start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), catchup=False, tags=["fake"])
def fake_person():

    @task()
    def extract(n) -> list:
        """
        Tâche d'extraction de l'équipe souhaitée
        """

        fake = Faker("fr_FR")

        return [
            {
                "Nom complet": fake.name(),
                "Date de naissance": fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%d/%m/%Y"),
                "Genre": random.choice(["Homme", "Femme"]),
                "Adresse": fake.address(),
                "Ville": fake.city(),
                "Code postal": fake.postcode(),
                "Pays": fake.country(),
                "Numéro de téléphone": fake.phone_number(),
                "Adresse e-mail": fake.email(),
                "Profession": fake.job(),
                "Entreprise": fake.company(),
                "Numéro de sécurité sociale": fake.ssn(),
                "Numéro de carte d'identité": fake.bothify(text="ID-########"),
                "Numéro de passeport": fake.bothify(text="P########"),
                "Date d'expiration du passeport": fake.date_this_decade().strftime("%d/%m/%Y"),
                "État civil": random.choice(["Célibataire", "Marié(e)", "Divorcé(e)", "Veuf(ve)"]),
                "Nombre d'enfants": random.randint(0, 4),
                "Taille (cm)": random.randint(150, 200),
                "Poids (kg)": random.randint(50, 100),
                "Groupe sanguin": random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
                "Couleur des yeux": random.choice(["Bleu", "Vert", "Marron", "Noisette", "Gris"]),
                "Couleur des cheveux": random.choice(["Blond", "Brun", "Noir", "Roux", "Châtain"]),
            }
            for _ in range(n)
        ]

    @task()
    def connect_and_insert(person_list: list):

        mongo_uri = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(mongo_uri)

        # Sélection de la base de données et de la collection
        db = client["test_db"]
        collection = db["fake_person"]

        # Insertion des données dans MongoDB
        collection.insert_many(person_list)

        # Fermeture de la connexion
        client.close()

    person_list = extract(100000)
    connect_and_insert(person_list)


# Lancement global de la fonction
fake_person()
