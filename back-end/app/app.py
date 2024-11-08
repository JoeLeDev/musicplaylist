from flask import Flask, request
from flask_cors import CORS
from .models import db
from .routes.song_routes import song_routes
from .routes.playlist_routes import playlist_routes
from .routes.spotify_routes import spotify_routes
from .config import Config  # Import de la configuration

app = Flask(__name__)
app.config.from_object(Config)  # Charger la configuration
CORS(app)

db.init_app(app)

# Enregistrer les routes
app.register_blueprint(song_routes)
app.register_blueprint(playlist_routes)
app.register_blueprint(spotify_routes)

# Route pour gérer les requêtes `OPTIONS` manuellement
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = app.make_response("")
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)

