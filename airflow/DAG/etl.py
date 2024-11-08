"""
Ce DAG va permettre d'extraire des données depuis une page WEB, de les transformer puis de les stocker au bon endroit dans le stockage local avant de faire des tests de BDD
"""

# Import des librairies nécessaires
from airflow.decorators import dag, task
import pendulum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import pymongo


@dag(schedule="@once", start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), catchup=False, tags=["regional_1_etl"])
def taskflow_regional():

    @task()
    def extract(path: str) -> dict:
        """
        Tâche d'extraction de l'équipe souhaitée
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # Configuration de Selenium avec ChromeDriver
        service = ChromeService(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # URL de la compétition
        driver.get(path)

        # Attendre que la page charge
        time.sleep(3)

        tab_selector = driver.find_elements(By.CLASS_NAME, "tabSelector")
        buttons = tab_selector[1].find_elements(By.TAG_NAME, "button")

        # Extraction des noms d'équipe
        equipe_1, equipe_2 = tab_selector[1].text.strip().split("\n")

        # Extraire la composition de la première équipe
        try:
            composition = {
                f"{equipe_1}": {f"{i}": driver.find_element(By.ID, f"poste_{i}").text.strip() for i in range(1, 23)}
            }
            pprint(composition)
        except Exception as e:
            print("Joueur non trouvé", e)

        button = buttons[1]
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()

        # Extraire la composition de la deuxième équipe
        try:
            composition[f"{equipe_2}"] = {
                f"{i}": driver.find_element(By.ID, f"poste_{i}").text.strip() for i in range(1, 23)
            }
            pprint(composition)
        except Exception as e:
            print("Joueur non trouvé", e)

        driver.quit()

        return composition

    @task()
    def transform_1(composition: dict) -> dict:
        """
        Tâche de modification de la donnée numéro 1
        """

        # Tâche de transformation de la donnée
        transformed_data = {
            team.lower(): {poste: joueur.upper().replace(" ", "") for poste, joueur in composition[team].items()}
            for team in composition
        }

        return transformed_data

    @task()
    def transform_2(composition: dict) -> dict:
        """
        Tâche de modification de la donnée numéro 2
        """

        # Tâche de transformation de la donnée
        transformed_data = {
            team.upper(): {
                poste: joueur.upper().replace(" ", "").split(".")[1] for poste, joueur in composition[team].items()
            }
            for team in composition
        }

        return transformed_data

    @task()
    def connect_and_insert(transformed_data: dict):
        # URL de connexion MongoDB (si MongoDB est sur le même serveur que Airflow)
        mongo_uri = "mongodb://localhost:27017/"

        # Connexion à la base de données MongoDB
        client = pymongo.MongoClient(mongo_uri)

        # Sélection de la base de données et de la collection
        db = client["test_db"]
        collection = db["compositions"]

        # Insertion des données dans MongoDB
        collection.insert_one(transformed_data)

        # Fermeture de la connexion
        client.close()

    # Test avec stockage en JSON
    # @task()
    # def load(transformed_data: dict, dir: str) -> None:
    #     """
    #     Tâche de chargement dans un fichier JSON de l'équipe souhaitée
    #     """

    #     # Création du repo s'il n'existe pas
    #     os.makedirs(os.path.dirname(dir), exist_ok=True)

    #     # Chargement des données
    #     with open(dir, "w") as outfile:
    #         json.dump(transformed_data, outfile)

    # Lancement des fonctions d'ETL

    # Extraction de la donnée
    composition = extract(
        "https://competitions.ffr.fr/competitions/nouvelle-aquitaine-regionale-1-championnat-territorial/match-1428351.html"
    )

    # Différentes transformations
    transformed_data_1 = transform_1(composition)
    # transformed_data_2 = transform_2(composition)

    # Transformation de la donnée
    # load(transformed_data_1, "airflow/data/data_1/data.json")
    # load(transformed_data_2, "airflow/data/data_2/data.json")

    # Chargement de la donnée
    connect_and_insert(transformed_data=transformed_data_1)


# Lancement global de la fonction
taskflow_regional()
