from flask import Flask
from .models import db  # ou importe db depuis models
from config import Config  # Si tu utilises un fichier de configuration séparé

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialiser les extensions
    db.init_app(app)

    # Enregistre les blueprints, s'il y en a
    from .routes import main  # exemple si tu as un blueprint main
    app.register_blueprint(main)

    return app
