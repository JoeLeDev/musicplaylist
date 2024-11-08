from flask import jsonify, request
from ..models import db, Playlist, PlaylistSong, Song
from sqlalchemy.exc import IntegrityError

def create_playlist():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Playlist name is required!'}), 400
    
    new_playlist = Playlist(name=data['name'])
    db.session.add(new_playlist)
    db.session.commit()
    return jsonify({'message': 'Playlist created successfully!', 'playlist_id': new_playlist.id}), 201

def add_song_to_playlist(playlist_id):
    data = request.json
    song_id = data.get('song_id')
    playlist = Playlist.query.get_or_404(playlist_id)
    song = Song.query.get_or_404(song_id)
    
    new_playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
    db.session.add(new_playlist_song)
    db.session.commit()
    return jsonify({'message': 'Song added to playlist successfully!'}), 200

def get_all_playlists():
    playlists = Playlist.query.all()
    if not playlists:
        return jsonify({'error': 'No playlists found'}), 404
    return jsonify([playlist.to_dict() for playlist in playlists])

def get_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist introuvable'}), 404

    songs = [
        {
            'id': ps.song.id,
            'name': ps.song.name,
            'artist': ps.song.artist,
            'album': ps.song.album
        }
        for ps in playlist.songs
    ]

    return jsonify({
        'id': playlist.id,
        'name': playlist.name,
        'songs': songs
    }), 200


def update_playlist_name(playlist_id):
    data = request.json
    new_name = data.get('name')
    if not new_name:
        return jsonify({'error': 'New playlist name is required!'}), 400

    playlist = Playlist.query.get_or_404(playlist_id)
    try:
        playlist.name = new_name
        db.session.commit()
        return jsonify({'message': 'Playlist name updated successfully!'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to update playlist name due to integrity constraint.'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update playlist name. Error: {str(e)}'}), 500

def delete_playlist(playlist_id):
    try:
        PlaylistSong.query.filter_by(playlist_id=playlist_id).delete()
        playlist = Playlist.query.get_or_404(playlist_id)
        db.session.delete(playlist)
        db.session.commit()
        return jsonify({'message': 'Playlist deleted successfully!'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete playlist due to database constraint.'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    

def update_song_in_playlist(playlist_id):
    data = request.json
    song_id = data.get('song_id')
    new_name = data.get('name')

    if not song_id or not new_name:
        return jsonify({'error': 'Song ID and new name are required!'}), 400

    playlist_song = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
    if not playlist_song:
        return jsonify({'error': 'Song not found in the specified playlist'}), 404

    try:
        song = Song.query.get(song_id)
        if not song:
            return jsonify({'error': 'Song not found'}), 404

        song.name = new_name
        db.session.commit()
        return jsonify({'message': 'Song name updated successfully in the playlist!'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to update song due to integrity constraint.'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update song. Error: {str(e)}'}), 500



def delete_song_from_playlist(playlist_id, song_id):
    try:
        # Rechercher et supprimer l'association entre la playlist et la chanson
        playlist_song = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
        if not playlist_song:
            return jsonify({'error': 'Chanson introuvable dans la playlist'}), 404

        db.session.delete(playlist_song)
        db.session.commit()
        return jsonify({'message': 'Chanson supprimée de la playlist avec succès'}), 200
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la suppression'}), 500
