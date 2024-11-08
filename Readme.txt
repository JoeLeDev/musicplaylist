README

Description de l'application

Cette application est une plateforme musicale permettant aux utilisateurs de rechercher des chansons via l'API Spotify, de les ajouter dans une base de données locale, de créer et gérer des playlists, et de voir des détails sur les playlists avec des options d'édition et de suppression. L'application se compose de deux parties : un backend construit avec Flask et un frontend simple en HTML/CSS/JavaScript.

Fonctionnalités principales

Recherche de chansons par artiste via l'API Spotify.

Ajout de chansons à une base de données locale.

Création, édition et suppression de playlists.

Affichage des détails des playlists, avec des options pour éditer ou supprimer des chansons.

Interface utilisateur intuitive avec gestion de la pagination et filtres de recherche.

Structure de l'application

Backend : Dossier back-end contenant l'application Flask avec les routes, la configuration et la gestion de la base de données.

Frontend : Dossier front-end contenant les fichiers HTML, CSS et JavaScript pour l'interface utilisateur.

Base de données : PostgreSQL est utilisée pour stocker les informations sur les chansons et les playlists.

Prérequis

Python 3.9 ou version ultérieure

Node.js pour exécuter le serveur HTTP local (http-server)

PostgreSQL installé et configuré

Installation et démarrage


Configurer l'environnement virtuel Python :

cd back-end
python3 -m venv venv
source venv/bin/activate  (Sur Windows : venv\Scripts\activate)
pip install -r requirements.txt

Connexion à la base de données :

Assurez-vous que PostgreSQL est en cours d'exécution et remplissez les informations de connexion dans le fichier .env. Pour vous connecter à la base de données via le terminal :

psql -h <hôte> -U <utilisateur> -d <nom_de_la_base>

Lancer le backend Flask :

flask run --host=0.0.0.0 --port=5002

Lancer le frontend :
Dans un nouveau terminal, déplacez-vous dans le dossier front-end et exécutez :

npx http-server -p 8081

Utilisation

Accédez au frontend via http://localhost:8081.

L'API backend est accessible sur http://localhost:5002.

Utilisez l'interface pour rechercher des chansons, créer des playlists et gérer les contenus.