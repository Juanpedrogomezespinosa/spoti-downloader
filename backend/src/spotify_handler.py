import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Usamos credenciales de cliente (perfecto para que el servidor no se bloquee)
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def obtener_canciones_spotify(url_spotify: str) -> dict:
    try:
        # Expresión regular infalible: Busca playlist, album o track y extrae solo su ID alfanumérico
        match = re.search(r"(playlist|album|track)/([a-zA-Z0-9]+)", url_spotify)
        
        if not match:
            print("No se encontró un ID válido en la URL.")
            return None
            
        tipo = match.group(1)
        item_id = match.group(2)
        
        # 1. SI ES UNA PLAYLIST
        if tipo == "playlist":
            info_playlist = sp.playlist(item_id, fields="name")
            nombre = info_playlist.get('name', 'Playlist')
            
            # Paginación para obtener TODAS las canciones (por si la lista es muy larga)
            resultados = sp.playlist_tracks(item_id)
            pistas = resultados.get('items', [])
            
            while resultados.get('next'):
                resultados = sp.next(resultados)
                pistas.extend(resultados['items'])
            
            lista_canciones = []
            for item in pistas:
                track = item.get('track')
                if track and track.get('name'):
                    nombre_cancion = track['name']
                    artistas = ", ".join([artista['name'] for artista in track.get('artists', [])])
                    lista_canciones.append(f"{nombre_cancion} {artistas} audio")
                    
            return {"nombre_carpeta": nombre, "canciones": lista_canciones}

        # 2. SI ES UN ÁLBUM
        elif tipo == "album":
            resultados = sp.album(item_id)
            nombre = resultados['name']
            pistas = resultados['tracks']['items']
            
            lista_canciones = []
            for track in pistas:
                nombre_cancion = track['name']
                artistas = ", ".join([artista['name'] for artista in track['artists']])
                lista_canciones.append(f"{nombre_cancion} {artistas} audio")
            return {"nombre_carpeta": nombre, "canciones": lista_canciones}

        # 3. SI ES UNA CANCIÓN SUELTA (TRACK)
        elif tipo == "track":
            track = sp.track(item_id)
            nombre_cancion = track['name']
            artistas = ", ".join([artista['name'] for artista in track['artists']])
            return {
                "nombre_carpeta": nombre_cancion, 
                "canciones": [f"{nombre_cancion} {artistas} audio"]
            }
            
    except Exception as e:
        print(f"Error procesando los datos de Spotify: {e}")
        return None