from flask import Blueprint
from ..controllers.song_controller import get_songs, add_songs_to_db, update_song, delete_song, get_songs_by_artist

song_routes = Blueprint('song_routes', __name__)

song_routes.route('/songs', methods=['GET'])(get_songs)
song_routes.route('/add_spotify_songs', methods=['POST'])(add_songs_to_db)
song_routes.route('/songs/<int:song_id>', methods=['PUT'])(update_song)
song_routes.route('/songs/<int:song_id>', methods=['DELETE'])(delete_song)
song_routes.route('/songs/filter', methods=['GET'])(get_songs_by_artist)

