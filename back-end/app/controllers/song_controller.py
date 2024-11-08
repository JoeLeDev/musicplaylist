from flask import jsonify, request
from ..models import db, Song, SongPopularity
from sqlalchemy.exc import IntegrityError
import traceback

def get_songs():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Pagination par ID pour une meilleure performance
        songs = Song.query.order_by(Song.id).paginate(page=page, per_page=per_page)
        result = [{'id': song.id, 'name': song.name, 'artist': song.artist, 'album': song.album} for song in songs.items]
        
        return jsonify({
            'songs': result,
            'total': songs.total,
            'pages': songs.pages,
            'page': songs.page,
            'per_page': songs.per_page
        }), 200
    except Exception as e:
        print(f"Erreur lors de la récupération des chansons : {traceback.format_exc()}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

def add_songs_to_db():
    try:
        data = request.json
        if not data or 'songs' not in data:
            return jsonify({'error': 'No songs provided!'}), 400
        
        songs = data['songs']
        if isinstance(songs, dict):
            songs = [songs]
        
        added_songs_count = 0

        for song in songs:
            # Utiliser indexation de `name` et `artist` pour une recherche rapide
            existing_song = Song.query.filter(
                Song.name.ilike(song['name']),
                Song.artist.ilike(song['artist'])
            ).first()
            
            if existing_song:
                print(f"La chanson '{song['name']}' de '{song['artist']}' est déjà présente dans la BDD.")
                continue

            new_song = Song(name=song['name'], artist=song['artist'], album=song.get('album'))
            db.session.add(new_song)
            added_songs_count += 1

        db.session.commit()

        if added_songs_count == 0:
            return jsonify({'message': 'Chanson déjà présente dans la base de données'}), 200
        else:
            return jsonify({'message': f"{added_songs_count} songs added to the database!"}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'ajout des chansons : {traceback.format_exc()}")
        return jsonify({'error': 'Internal Server Error'}), 500

def update_song(song_id):
    song = Song.query.get_or_404(song_id)
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided to update the song.'}), 400
    
    try:
        song.name = data.get('name', song.name)
        song.artist = data.get('artist', song.artist)
        song.album = data.get('album', song.album)
        db.session.commit()
        return jsonify({'message': 'Song updated successfully!'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to update the song due to integrity constraint.'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la mise à jour de la chanson : {traceback.format_exc()}")
        return jsonify({'error': f'Failed to update the song. Error: {str(e)}'}), 500

def delete_song(song_id):
    try:
        song = Song.query.get_or_404(song_id)
        db.session.delete(song)
        db.session.commit()
        return jsonify({'message': 'Song deleted successfully!'}), 200
    except IntegrityError:
        db.session.rollback()
        print(f"Erreur lors de la suppression de la chanson : {traceback.format_exc()}")
        return jsonify({'error': 'Failed to delete the song.'}), 500

def get_songs_by_artist():
    artist_name = request.args.get('artist', '').lower()
    if not artist_name:
        return jsonify({"error": "Artist name is required"}), 400

    try:
        # Rechercher les chansons correspondant à l'artiste, en utilisant un index sur artist
        songs = Song.query.filter(Song.artist.ilike(f"%{artist_name}%")).all()
        songs_list = [{'id': song.id, 'name': song.name, 'artist': song.artist, 'album': song.album} for song in songs]

        return jsonify(songs_list), 200
    except Exception as e:
        print(f"Erreur lors de la recherche de chansons par artiste : {traceback.format_exc()}")
        return jsonify({"error": "Erreur interne du serveur"}), 500
