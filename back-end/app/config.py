import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()


class Config:
    # Charger les variables d'environnement pour la base de données
    DB_USERNAME = os.getenv('DB_USERNAME') 
    DB_PASSWORD = os.getenv('DB_PASSWORD') 
    DB_HOST = os.getenv('DB_HOST') 
    DB_NAME = os.getenv('DB_NAME')

    # Construire la chaîne de connexion à la base de données
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
