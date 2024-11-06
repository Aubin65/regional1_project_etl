"""
Cette partie est utilisée pour extraire la donnée depuis le site de la FFR
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import luigi
import json
import pandas

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
        Cette fonction enregistre les données extraites au format JSON de manière temporaire
        """
        return luigi.LocalTarget("extracted_data.json")

    def run(self):

        chrome_options = Options()
        chrome_options.add_argument("--headless")


        # Configuration de Selenium avec ChromeDriver
        service = ChromeService(executable_path='/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Remplacez par l'URL que vous souhaitez visiter
        url_match = "https://competitions.ffr.fr/competitions/nouvelle-aquitaine-regionale-1-championnat-territorial/match-1428351.html"  # Remplacez cette URL par celle que vous voulez
        driver.get(url_match)

        # Attendez que le JavaScript se charge
        time.sleep(3)  # Ajustez ce temps selon vos besoins

        tab_selector = driver.find_elements(By.CLASS_NAME, "tabSelector")
        buttons = tab_selector[1].find_elements(By.TAG_NAME, "button")

        equipe_1, equipe_2 = tab_selector[1].text.strip().split("\n")
        print(f"Equipe 1 : {equipe_1}\nEquipe 2 : {equipe_2}")

        #Extraire la composition
        try:
            composition = {f"{equipe_1}" : {f"{i}" : driver.find_element(By.ID, f'poste_{i}').text.strip() for i in range(1,23)}}
            pprint(composition)
        except Exception as e:
            print("Joueur non trouvé", e)

        button = buttons[1]
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()

        #Extraire la composition
        try:
            composition = {f"{equipe_2}" : {f"{i}" : driver.find_element(By.ID, f'poste_{i}').text.strip() for i in range(1,23)}}
            pprint(composition)
        except Exception as e:
            print("Joueur non trouvé", e)

        with self.output().open('w') as f:
            json.dump(composition, f, indent=4)

        driver.quit()

