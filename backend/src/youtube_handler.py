import yt_dlp
import os

def descargar_cancion(busqueda: str, carpeta_destino: str):
    """
    Busca el texto en YouTube y descarga el audio en MP3.
    """
    consulta = f"ytsearch1:{busqueda}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        # Esta es la magia para pasarlo a MP3
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
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