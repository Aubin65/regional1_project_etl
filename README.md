# regional1_project

Ce repository est utilisé pour alimenter la base de données contenant les données du championnat régionale 1 de rugby pour la saison 2023-2024

Les technos utilisées seront PostgreSQL et Python. Les scripts seront orchestrés par Apache Airflow et la base de données sera hébergée sur une Raspberry Pi 4.


## **Doc**

<u>Pour installer chrome sous un WSL :</u> 

```bash
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```


<u>Pour installer le webdriver :</u>  

Trouver sa version de chrome : google-chrome --version

Trouver la version associée du webdriver : `https://developer.chrome.com/docs/chromedriver/downloads/version-selection?hl=fr`

Par ex : `https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.69/linux64/chromedriver-linux64.zip`

```bash
sudo wget https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.69/linux64/chromedriver-linux64.zip
sudo unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
sudo rm -rf chromedriver-linux64.zip chromedriver-linux64
sudo chmod +x /usr/local/bin/chromedriver
chromedriver --version
```

Le chemin du fichier chromedriver est a utiliser dans la ligne de code suivante : 

```python
service = ChromeService(executable_path='/chemin/vers/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)
```

<u>Pour communiquer entre PostgreSQL et Python :</u> 

```bash
# Installation de la librairie
pip install psycopg2-binary
```

```python
import psycopg2

# Connexion à la base de données
conn = psycopg2.connect(
    dbname="ma_base",
    user="mon_utilisateur",
    password="mon_mot_de_passe",
    host="localhost",
    port="5432"
)

# Création d'un curseur pour exécuter des commandes SQL
cursor = conn.cursor()

# Exécution d'une requête
cursor.execute("SELECT * FROM ma_table;")

# Récupération des résultats
rows = cursor.fetchall()

for row in rows:
    print(row)

# Fermeture du curseur et de la connexion
cursor.close()
conn.close()
```