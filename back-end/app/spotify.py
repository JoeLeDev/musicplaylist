import requests
import base64
import os
import time
from dotenv import load_dotenv
load_dotenv()

# Variable globale pour stocker le token et son expiration
spotify_token = None
token_expiration_time = 0

# Fonction pour obtenir un token d'accès Spotify
def get_spotify_token():
    global spotify_token
    global token_expiration_time

    # Si le token est encore valide, on le retourne
    if spotify_token and time.time() < token_expiration_time:
        return spotify_token

    # Sinon, on demande un nouveau token
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    # Encoder le client_id et le client_secret en Base64
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    
    # Headers pour la requête POST
    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Données de la requête
    data = {
        'grant_type': 'client_credentials'
    }
    
    # Faire la requête POST pour obtenir le token
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    response_data = response.json()

    # Stocker le token et son heure d'expiration (3600 secondes = 1 heure)
    spotify_token = response_data['access_token']
    token_expiration_time = time.time() + response_data['expires_in'] - 60  # On enlève 60 secondes pour être prudent

    # Retourner le token d'accès
    return spotify_token


# Fonction pour récupérer des chansons par artiste
def get_spotify_songs(artist_name, page=1, limit=10):
    token = get_spotify_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    offset = (page - 1) * limit  # Calculer l'offset pour la pagination

    search_url = 'https://api.spotify.com/v1/search'
    params = {
        'q': artist_name,
        'type': 'track',
        'limit': limit,
        'offset': offset
    }
    
    response = requests.get(search_url, headers=headers, params=params)
    
    # Vérifier si la requête est réussie
    if response.status_code == 200:
        songs = response.json()['tracks']['items']
        
        result = []
        for song in songs:
            result.append({
                'name': song['name'],
                'album': song['album']['name'],
                'artist': song['artists'][0]['name'],
                'popularity': song['popularity']
            })

        return result
    else:
        return None

# Test
if __name__ == "__main__":
    artist = "Chris Brown"
    songs = get_spotify_songs(artist)
    
    if songs:
        for song in songs:
            print(f"Title: {song['name']}, Album: {song['album']['name']}, Artist: {song['artists'][0]['name']}, Popularity: {song['popularity']}")
    else:
        print(f"Could not fetch songs for artist {artist}")
