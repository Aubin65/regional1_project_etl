Ce fichier est utilisé pour prendre des notes sur le projet. 
La première chose à ajouter est d'utiliser le cache de streamlit pour les données de connexion à la base de données PostgreSQL.

Réflexion sur le sujet 28/10 : 

Idée : faire une BDD Postgre qui va contenir les résultats des matchs de la poule de régionale 1

Idées : 

	• Graphe d'évolution du score
	• Compositions avec temps de jeu global des joueurs, % de titularisation, ancienneté dans le club, nombre de points marqués au global -> isoler chaque joueur sur une autre page
	• Statistiques perso du joueur : Cliquer sur le joueur qui est représenté sur le terrain 
	• Stats globales de l'équipe : nombre de points marqués, nombre d'essais, % des essais marqués dans telle tranche de temps du match
	• Classements des équipes
	• Temps de jeu de chaque joueur pour le match
	• Ajouter lien vers la vidéo du match
	• Pour chaque joueur -> id, nom, prénom, nom_ancien_club, anciennete_club
	• Pour chaque match -> id, id_composition_equipe_1, nom_equipe_1, cartons_jaunes_equipe_1, nom_equipe_1
	• Composition -> id, id_match, numéro_joueur, id_joueur
	• Actions : type (remplacement, pénalité, essai), minute, points, id_joueur,  id_equipe; id_match. nb : séparer entrée / sortie du joueur ?

Pour avoir le nombre de pts marqués par une équipe dans un match spécifique: 

```sql
SELECT SUM(points)
FROM Actions
WHERE (id_match="selected_match") AND (id_equipe=(SELECT id FROM match WHERE nom_equipe_1="RCUJ"));
```

Idées de stratégie pour ne pas collecter plusieurs fois les mêmes données :

* Stocker les URLs dans la base de données PostgreSQL (par exemple lié aux équipes), scrapper seulement si l'URL n'est pas dans la table URL
	* Question : est-ce qu'on crée une table url ou est-ce qu'on met l'url dans la table match, qu'on viendra requêter ?
		* Piste : Je pense que c'est mieux de le mettre dans la table match car on peut faire un 
		```sql
		SELECT DISTINCT(url)
		FROM match;
		```