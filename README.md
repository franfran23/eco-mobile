# Eco-mobile
## Presentaion du Projet
Eco-Mobile est un site de Covoiturage créé pour les membres de l'enseignement à l'EIC dans le but de faciliter le trajet amenant au lycée afin de désengorger le trafic routier ainsi que de réduire le taux d'emmision de gaz a effet de serre.

Ce projet à été imaginé par les éleves de Terminale de la filière Professionnelle dans le cadre de leur chef-d'oeuvre et développé par des Terminales dans le cadre de la spéciailité NSI.

Ce projet est voué à évoluer et être amélioré grâce aux éléves volontaires de la spétialité NSI

## Documentaion
### Presentaion PDF du Projet
- https://drive.google.com/file/d/1KzbczTO7kPLg5W2m3l6jtp6aXVcfHa1e/view?usp=sharing
### Maquette Figma
- https://www.figma.com/design/hUS6Kx48YHU2iJ5T4XY9mr/Maquette-covoit?t=s9rQkhk0ho0aDUd8-1

# Petit Guide de Démarrage : 
## Comment utiliser GitHub ?
### Comment coder ?
Il suffit d'appuyer sur le bouton vert '<> Code', puis aller dans la section Codespaces et créer son codesapace.
### Comment voir les changements que je suis entrain de coder sur le site ?
Entrez la comande suivante dans le terminal: `python3 main.py`
Puis un popup và s'ouvrir vous pouvez cliquer sur 'ouvrir dans un navigateur' une nouvelle fenêtre và s'ouvrir.
### Comment envoyer mes modifications et recevoir les dernières modification enregistrées?
Allez dans le troisième onglet vertical à gauche de votre écran puis appuyer sur le bouton 'validation' puis entrez votre commit (les modification que vous avez apportez) pour ensuite valider.

(ou simplement depuis le terminal avec la commande suivante: `git push` (pour envoyer) et `git pull` (pour recevoir))

Noubliez pas de syncroniser les modifications.


# Info Commits
format de l'adresse mail pour le code de validation à définir (pour garder une cohérence avec une éventuelle adresse de contact) --> demander au client 

# todo list
## frontend
- [x] page d'accueil  
- [x] page de connexion  
- [x] page d'inscription  
- [x] page de messagerie
- [x] Il faudra ajouter une page avec un message ({{ }}, formatage python) et un input pour un nombre entier: code de vérification par email (verif.html ?)
cette page contiendra un formulaire post avec un élément caché nommé "username" dont la valeur sera {{ username }}. L'input pour le code aura le nom "code"
- [x] Update de inscription.html pour ajouter la sélection de la zone géographique (name="zone") et des horaires de cours (à voir comment c'est mis en place)

- [ ] Page verif faire fonctionner les bouttons en plus
- [x] Les messages dépassent du chat quand il y en as bcp
- [x] Ajouter un id différent pour les messages envoyés et les messages reçus pour pouvoir les différencier
- [ ] refont de la page d'accueil (virer tout le absolute -> page responsive)

## backend
- [x] système de login
- [x] système d'inscription (update en cours mais fonctionnel)
- [x] messagerie
- [x] update signup pour enregistrer la zone géographique et les horaires de cours
- [x] update la requête de création de la table identifiants pour inclure l'id de la zone géographique (quand la table zone sera créée)
- [x] (si les messages doivent être cryptés dans la db, trouver un format pour générer les clés, ex: utiliser les id des utilisateurs comme graine de génération d'une clé (le résultat sera toujours le même))
- [x] calcul de qui est compatible au covoiturage  
- [ ] Sauvegarder les messages dans le chat
- [ ] créer un smtp pour la connexion avec les e-mails
- [ ] ajouter un mdp oublié ?
- [ ] faire fonctionner le message de notification + (dans terminal ne pas oublier d'installer les modules: `pip install notify-py` )

## DataBase
(créer un fichier .txt avec toutes les requêtes de création de tables, une par ligne)  
- Ecrire les requêtes sql pour:  
  - [x] créer la table horaires:  
    - id unique auto incrémenté  
    - id de l'utilisateur (clé secondaire)  
    - une colonne pour chaque jours de la semaine  
    - horaires formatés (ex: "08:00/18:00")  
    - prendre en compte les semaines A/B ? (créer d'autres colonnes ou utiliser un formatage différent, ex: "08:00/18:00//09:00/17:00" (semA//semB))  
  - [ ] créer la table messages:  
    - id unique autoincrémenté  
    - id de l'émetteur du message (id d'utilisateur, clé secondaire)  
    - id du receveur (same)  
    - contenu du msg (éventuellement crypté)  
    - date/heure du msg (timestamp) (pour récupérer les msg dans l'ordre)  
    - (statut du message (lu/non lu))  
  - [x] créer la table zone:  
    - id unique autoincrémenté  
    - nom de la zone (ex: Tourcoing Nord-Est) (les zones seront dabord définies manuellement, puis éventuellement automatisées avec une API google Maps par exemple)  

[ ] Récupérer les n derniers messages entre user1 et user2 (donc triés par date)  


# Auteurs
## Idée du Projet
* **DELVALLEE Thomas**
* **DELLI Nelya**
* **DEMEYER Rachel**
* **HARIRECHE Kahina**
* **ZOUARI Ines**

## Developpement
* **CAUS François** _alias_ [@franfran23](https://github.com/franfran23)
* **DESTAILLEUR Simon** _alias_ [@6mond](https://github.com/6mond)
* **GHAZLI Abdelilah** _alias_ [@AbdeGzl](https://github.com/AbdeGzl)
* **VANBREMEERSCH Eric** _alias_ [@Eric-Vanbremeersch](https://github.com/Eric-Vanbremeersch)

Merci du Soutien que nous as apporté Mme Julien ainsi que les membres du Cube-EIC.