from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)  
    artist = db.Column(db.String(100), nullable=False, index=True)  
    album = db.Column(db.String(100), nullable=True)
    playlists = db.relationship('PlaylistSong', backref='song', cascade="all, delete", lazy=True)


class SongPopularity(db.Model):
    __tablename__ = 'song_popularity'
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False, index=True)  # Index sur song_id
    popularity_score = db.Column(db.Integer, nullable=False)

    song = db.relationship('Song', backref=db.backref('popularity', lazy=True))


class Playlist(db.Model):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    songs = db.relationship('PlaylistSong', backref='playlist', cascade="all, delete-orphan", lazy=True)

    # Ajout de la méthode to_dict
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class PlaylistSong(db.Model):
    __tablename__ = 'playlist_song'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False, index=True)  
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False, index=True) 
