"""
Ce DAG va permettre d'extraire des données depuis une page WEB, de les transformer puis de les stocker au bon endroit dans le stockage local avant de faire des tests de BDD
"""

# Import des librairies nécessaires
import json
from airflow.decorators import dag, task
import pendulum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from pprint import pprint


@dag(schedule=None, start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), catchup=False, tags=["regional_1_etl"])
def taskflow_regional():

    @task()
    def extract() -> dict:
        """
        Tâche d'extraction de l'équipe souhaitée
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # Configuration de Selenium avec ChromeDriver
        service = ChromeService(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Remplacez par l'URL que vous souhaitez visiter
        url_match = "https://competitions.ffr.fr/competitions/nouvelle-aquitaine-regionale-1-championnat-territorial/match-1428351.html"  # Remplacez cette URL par celle que vous voulez
        driver.get(url_match)

        # Attendez que le JavaScript se charge
        time.sleep(3)  # Ajustez ce temps selon vos besoins

        tab_selector = driver.find_elements(By.CLASS_NAME, "tabSelector")
        buttons = tab_selector[1].find_elements(By.TAG_NAME, "button")

        equipe_1, equipe_2 = tab_selector[1].text.strip().split("\n")

        # Extraire la composition
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

        # Extraire la composition
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
    def transform(composition: dict) -> dict:
        """
        Cette fonction va venir ouvrir le fichier de stockage temporaire en json et y apporter les modifications nécessaires :
            - Passer les noms des joueurs en majuscules et enlever les espaces entre l'initiale et le nom
            - Passer les noms des clubs en minuscule
        """

        transformed_data = {
            team.lower(): {poste: joueur.upper().replace(" ", "") for poste, joueur in composition[team].items()}
            for team in composition
        }

        return transformed_data

    @task()
    def load(transformed_data: dict) -> None:
        """
        Tâche de chargement dans un fichier JSON de l'équipe souhaitée
        """
        with open("airflow/data/data.json", "w") as outfile:
            json.dump(transformed_data, outfile)

    composition = extract()
    transformed_data = transform(composition)
    load(transformed_data)


taskflow_regional()
