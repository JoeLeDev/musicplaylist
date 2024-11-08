import sys
import time
from flask import Flask, request, g
from flask_cors import CORS
from .models import db
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from .routes.playlist_routes import playlist_routes
from .routes.song_routes import song_routes
from .routes.spotify_routes import spotify_routes
from .config import Config  # Import correct de la classe Config

# Charger les variables d'environnement depuis .env
load_dotenv()

# Désactiver le buffering pour afficher immédiatement les logs dans la console
sys.stdout = sys.stderr = open(sys.stdout.fileno(), 'w', buffering=1)

def create_app():
    # Créer l'application Flask
    app = Flask(__name__)

    # Charger la configuration depuis app/config.py
    app.config.from_object(Config)  # Correction ici

    # Accepter les requêtes du serveur front-end
    CORS(app)

    # Mesurer le temps avant chaque requête
    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            print(f"Requête pour {request.path} a pris {duration:.2f} secondes")
        return response

    # Initialiser la base de données
    db.init_app(app)

    # Initialiser Flask-Migrate
    migrate = Migrate(app, db)

    app.register_blueprint(playlist_routes)
    app.register_blueprint(song_routes)
    app.register_blueprint(spotify_routes)

    return app
