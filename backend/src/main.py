# backend/src/main.py
import os
import shutil
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Importamos nuestros módulos
from src.spotify_handler import obtener_canciones_spotify
from src.youtube_handler import descargar_cancion

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"], # Tu frontend de Astro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PeticionDescarga(BaseModel):
    url: str

def limpiar_archivos_temporales(ruta_carpeta: str, ruta_zip: str):
    """Borra la carpeta temporal y el ZIP después de enviarlo al usuario"""
    if os.path.exists(ruta_carpeta):
        shutil.rmtree(ruta_carpeta)
    if os.path.exists(ruta_zip):
        os.remove(ruta_zip)

@app.post("/descargar")
async def descargar_playlist(peticion: PeticionDescarga, background_tasks: BackgroundTasks):
    url = peticion.url
    
    # 1. Obtener datos de Spotify
    datos_spotify = obtener_canciones_spotify(url)
    if not datos_spotify or len(datos_spotify["canciones"]) == 0:
        raise HTTPException(status_code=400, detail="No se encontraron canciones en esta URL de Spotify.")
    
    nombre_carpeta = datos_spotify["nombre_carpeta"]
    canciones = datos_spotify["canciones"]
    
    # 2. Crear carpeta temporal para las descargas
    ruta_temp = f"./{nombre_carpeta.replace(' ', '_')}"
    os.makedirs(ruta_temp, exist_ok=True)
    
    # 3. Descargar cada canción desde YouTube
    for cancion in canciones:
        descargar_cancion(cancion, ruta_temp)
        
    # 4. Comprimir en un archivo .ZIP
    ruta_zip_base = f"./{nombre_carpeta.replace(' ', '_')}"
    shutil.make_archive(ruta_zip_base, 'zip', ruta_temp)
    ruta_zip_final = f"{ruta_zip_base}.zip"
    
    # 5. Programar la limpieza para que se borren del servidor al terminar
    background_tasks.add_task(limpiar_archivos_temporales, ruta_temp, ruta_zip_final)
    
    # 6. Enviar el archivo ZIP al navegador del usuario
    return FileResponse(
        path=ruta_zip_final, 
        media_type="application/zip", 
        filename=f"{nombre_carpeta}.zip"
    )