import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth  # <-- Cambiamos la librería de autenticación
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Configurar Spotify con autenticación de USUARIO (abrirá el navegador)
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:8000/callback",
    scope="playlist-read-private"  # Permiso mágico para leer todo
)
sp = spotipy.Spotify(auth_manager=auth_manager)

def obtener_canciones_spotify(url_spotify: str) -> dict:
    """
    Detecta si la URL es una canción, álbum o playlist,
    y devuelve una lista formateada para buscar en YouTube.
    """
    try:
        # Extraer el ID limpiando la URL
        item_id = url_spotify.split("/")[-1].split("?")[0]
        
        # 1. SI ES UNA PLAYLIST
        if "/playlist/" in url_spotify:
            # Pedimos el nombre por un lado
            info_playlist = sp.playlist(item_id, fields="name")
            nombre = info_playlist.get('name', 'Playlist')
            
            # Y pedimos las canciones por otro (¡Esto evita el fallo que teníamos!)
            resultados = sp.playlist_tracks(item_id)
            pistas = resultados.get('items', [])
            
            lista_canciones = []
            for item in pistas:
                track = item.get('track')
                # Verificamos que sea una canción real y no un podcast o archivo local vacío
                if track and track.get('name'):
                    nombre_cancion = track['name']
                    artistas = ", ".join([artista['name'] for artista in track.get('artists', [])])
                    lista_canciones.append(f"{nombre_cancion} {artistas} audio")
                    
            return {"nombre_carpeta": f"Playlist - {nombre}", "canciones": lista_canciones}

        # 2. SI ES UN ÁLBUM
        elif "/album/" in url_spotify:
            resultados = sp.album(item_id)
            nombre = resultados['name']
            pistas = resultados['tracks']['items']
            
            lista_canciones = []
            for track in pistas:
                nombre_cancion = track['name']
                artistas = ", ".join([artista['name'] for artista in track['artists']])
                lista_canciones.append(f"{nombre_cancion} {artistas} audio")
            return {"nombre_carpeta": f"Album - {nombre}", "canciones": lista_canciones}

        # 3. SI ES UNA CANCIÓN SUELTA (TRACK)
        elif "/track/" in url_spotify:
            track = sp.track(item_id)
            nombre_cancion = track['name']
            artistas = ", ".join([artista['name'] for artista in track['artists']])
            return {
                "nombre_carpeta": f"Cancion - {nombre_cancion}", 
                "canciones": [f"{nombre_cancion} {artistas} audio"]
            }
            
        else:
            print("URL no reconocida. Usa enlaces de Playlists, Álbumes o Canciones.")
            return None
            
    except Exception as e:
        print(f"Error procesando los datos de Spotify: {e}")
        return None

# --- Bloque de prueba ---
if __name__ == "__main__":
    url_prueba = input("👉 Pega un enlace de Canción, Álbum o Playlist y pulsa Enter: ")
    print("\nBuscando datos...")
    
    datos = obtener_canciones_spotify(url_prueba)
    
    if datos:
        print(f"\n🎵 ¡Éxito! Se creará la carpeta: {datos['nombre_carpeta']}")
        print(f"✅ Se van a procesar {len(datos['canciones'])} audios. Aquí tienes los primeros:")
        for cancion in datos['canciones'][:5]:
            print(f"  - {cancion}")
    else:
        print("\n❌ Fallo en la extracción.")