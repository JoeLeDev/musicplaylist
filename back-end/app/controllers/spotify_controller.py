from flask import jsonify, request
from ..spotify import get_spotify_songs, get_spotify_token

def get_spotify_songs_by_artist():
    artist = request.args.get('artist')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    if not artist:
        return jsonify({'error': 'Artist name is required!'}), 400

    offset = (page - 1) * limit
    songs = get_spotify_songs(artist)
    
    if songs:
        return jsonify({'songs': songs, 'page': page, 'limit': limit}), 200
    else:
        return jsonify({'error': 'Could not fetch songs from Spotify'}), 500
