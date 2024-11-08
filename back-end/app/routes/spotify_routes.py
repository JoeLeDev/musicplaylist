from flask import Blueprint
from ..controllers.spotify_controller import get_spotify_songs_by_artist

spotify_routes = Blueprint('spotify_routes', __name__)

spotify_routes.route('/spotify_songs', methods=['GET'])(get_spotify_songs_by_artist)
