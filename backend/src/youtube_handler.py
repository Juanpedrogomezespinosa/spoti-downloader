# backend/src/youtube_handler.py
import yt_dlp
import os

def descargar_cancion(busqueda: str, carpeta_destino: str):
    """
    Busca el texto en YouTube y descarga el mejor audio disponible.
    """
    # El prefijo ytsearch1: le dice que busque y se quede con el 1º resultado
    consulta = f"ytsearch1:{busqueda}"
    
    ydl_opts = {
        'format': 'm4a/bestaudio/best', # Formato seguro sin necesidad de conversores extra
        'outtmpl': os.path.join(carpeta_destino, '%(title)s.%(ext)s'),
        'quiet': False,
        'nocheckcertificate': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([consulta])
        return True
    except Exception as e:
        print(f"Error al descargar {busqueda}: {e}")
        return False