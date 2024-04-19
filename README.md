# Eco-mobile


format de l'adresse mail pour le code de validation à définir (pour garder une cohérence avec une éventuelle adresse de contact) --> demander au client 

la table contact ne sera peut être pas nécéssaire (ou alors pour stocker les clés de déchiffrage des messages entre user1 et user2 (dans ce cas (user1, user2) sera la clé principale et la clé de lecture des messages sera cryptée avec la masterkey)

# todo list
## frontend
- [x] page d'accueil  
- [x] page de connexion  
- [x] page d'inscription  
- [ ] page de messagerie
- [ ] Il faudra ajouter une page avec un message ({{ }}, formatage python) et un input pour un nombre entier: code de vérification par email (verif.html ?)
cette page contiendra un formulaire post avec un élément caché nommé "username" dont la valeur sera {{ username }}. L'input pour le code aura le nom "code"
- [ ] Update de inscription.html pour ajouter la sélection de la zone géographique et des horaires de cours


## backend
- [x] système de login
- [x] système d'inscription (update en cours mais fonctionnel)
- [ ] messagerie
- [ ] update signup pour enregistrer la zone géographique et les horaires de cours
- [ ] update la requête de création de la table identifiants pour inclure l'id de la zone géographique (quand la table zone sera créée)
- [ ] (si les messages doivent être cryptés dans la db, trouver un format pour générer les clés, ex: utiliser les id des utilisateurs comme graine de génération d'une clé (le résultat sera toujours le même))

## DataBase
(créer un fichier .txt avec toutes les requêtes de création de tables, une par ligne)  
- Ecrire les requêtes sql pour:
  - créer la table horaires:
    - id unique auto incrémenté
    - id de l'utilisateur (clé secondaire)
    - une colonne pour chaque jours de la semaine
    - horaires formatés (ex: "08:00/18:00")
    - prendre en compte les semaines A/B ? (créer d'autres colonnes ou utiliser un formatage différent, ex: "08:00/18:00//09:00/17:00" (semA//semB))
  - créer la table messages:
    - id unique autoincrémenté
    - id de l'émetteur du message (id d'utilisateur, clé secondaire)
    - id du receveur (same)
    - contenu du msg (éventuellement crypté)
    - date/heure du msg (timestamp) (pour récupérer les msg dans l'ordre)
    - (statut du message (lu/non lu))
  - créer la table zone:
    - id unique autoincrémenté
    - nom de la zone (ex: Tourcoing Nord-Est) (les zones seront dabord définies manuellement, puis éventuellement automatisées avec une API google Maps par exemple)

  - Récupérer les n derniers messages entre user1 et user2 (donc triés par date)


