*21/10 :*
* Début du projet
* Création du repo GitHub

*22/10 :*
* Tests des fonctions de web scrapping avec requests / BeautifulSoup
* Accès seul à la page HTML du site web sans les éléments dynamiques -> problème

*24/10 :*
* Réception de la Raspberry Pi 4 Model B
* Montage du boîtier pour la Raspberry Pi

*25/10 :*
* Ajout de la doc pour installer google chrome + chromedriver depuis un terminal bash
* Test des fonctions avec selenium pour selectionner éléments dynamiques sur un site web
 
*26/10 :*
* Connection SSH à la Raspberry PI
* Ajout de la doc

*28/10 :*
* Ajout de la récupération des informations de la partie "match" de la page dans le fichier [exploration.ipynb](https://github.com/Aubin65/regional1_project_etl/blob/test_branch/exploration/exploration.ipynb)

*29/10 :*
* Ajout de la récupération de l'url spécifique au joueur, manque à récupérer cela pour les deux équipes et pas seulement pour une 

*30/10 :*
* Ajout de la récupération des deux équipes. Pour cela, il faut s'attarder sur la classe tabSelector qui contient deux éléments, le deuxième contenant les boutons avec les noms d'équipes et les switch entre les deux pages lorsque l'on clique dessus. Il faut aussi bien faire défiler la page avant d'utiliser button.click() sinon la fonction ne fonctionne pas

*04/11 :*
* Ajout de la récupération de l'historique des clubs du joueur dans le fichier [exploration.ipynb](https://github.com/Aubin65/regional1_project_etl/blob/test_branch/exploration/exploration.ipynb)
* Ajout des fichiers data model ([.png](https://github.com/Aubin65/regional1_project_etl/blob/test_branch/project_management/data_model.png) et [.odp](https://github.com/Aubin65/regional1_project_etl/blob/test_branch/project_management/data_model.odp))

*20/11 :*
* Ajout de documentation dans le fichier [README.md](https://github.com/Aubin65/regional1_project_etl/blob/test_branch/README.md)
* Ajout du fichier [psql_functions.py](https://github.com/Aubin65/regional1_project_etl/blob/test_branch/src/psql_functions.py) initialisant les fonctions de connexion et déconnexion à la base de donnée PostgreSQL via Python