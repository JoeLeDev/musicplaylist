from flask import Blueprint
from ..controllers.playlist_controller import (
    create_playlist, add_song_to_playlist, get_all_playlists,
    get_playlist, update_playlist_name, delete_playlist,delete_song_from_playlist,update_song_in_playlist
)

playlist_routes = Blueprint('playlist_routes', __name__)

playlist_routes.route('/playlists', methods=['POST'])(create_playlist)
playlist_routes.route('/playlists/<int:playlist_id>/add_song', methods=['POST'])(add_song_to_playlist)
playlist_routes.route('/playlists', methods=['GET'])(get_all_playlists)
playlist_routes.route('/playlists/<int:playlist_id>', methods=['GET'])(get_playlist)
playlist_routes.route('/playlists/<int:playlist_id>', methods=['PUT'])(update_playlist_name)
playlist_routes.route('/playlists/<int:playlist_id>', methods=['DELETE'])(delete_playlist)
playlist_routes.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=['DELETE'])(delete_song_from_playlist)
playlist_routes.route('/playlists/<int:playlist_id>/song/<int:song_id>', methods=['PUT'])(update_song_in_playlist)
