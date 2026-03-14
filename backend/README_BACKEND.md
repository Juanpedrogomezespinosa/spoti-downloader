# 🎵 Proyecto: Descargador Educativo de Playlists

Bienvenido a este proyecto educativo. El objetivo es construir un programa en Python que reciba un enlace de una Playlist de Spotify y descargue las canciones automáticamente en una carpeta con el nombre de dicha Playlist.

**Arquitectura del Proyecto:**
Como los archivos de Spotify están encriptados con DRM, usaremos una arquitectura de dos fases:

1. Leeremos los metadatos (Nombres de canciones) de **Spotify**.
2. Buscaremos esos nombres y descargaremos el audio desde **YouTube**.

## 🛠️ Herramientas y Librerías necesarias

- **Editor:** Visual Studio Code (VS Code).
- **Lenguaje:** Python 3.
- **Librerías externas:**
  - `spotipy`: Para conectarnos a la API de Spotify y leer las listas.
  - `yt-dlp`: Para descargar el audio de YouTube.
  - `python-dotenv`: Para ocultar nuestras contraseñas y claves de API.

## 📝 Paso a Paso del Desarrollo

### Fase 1: Preparación del Entorno

1. Crea la estructura de carpetas indicada en este repositorio.
2. Abre la terminal en VS Code y crea un entorno virtual: `python -m venv venv`
3. Activa el entorno virtual.
4. Instala las dependencias necesarias: `pip install spotipy yt-dlp python-dotenv`
5. Guarda las dependencias en un archivo: `pip freeze > requirements.txt`

### Fase 2: Conexión con Spotify (`src/spotify_handler.py`)

1. Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), crea una App y obtén tu `Client ID` y `Client Secret`.
2. Guarda estas claves en un archivo llamado `.env` en la raíz del proyecto.
3. Programa una función que reciba una URL de Spotify, se autentique, y devuelva el **Nombre de la Playlist** y una **Lista con los nombres de las canciones y artistas**.

### Fase 3: Gestión de Carpetas (`src/folder_manager.py`)

1. Importa la librería estándar `os` o `pathlib`.
2. Programa una función que reciba el "Nombre de la Playlist".
3. La función debe comprobar si ya existe una carpeta con ese nombre dentro del directorio `descargas/`. Si no existe, debe crearla.

### Fase 4: Descarga de Audio (`src/youtube_handler.py`)

1. Importa la librería `yt-dlp`.
2. Programa una función que reciba el nombre de una canción (Ej: "Queen Bohemian Rhapsody") y la ruta de la carpeta que acabamos de crear.
3. Configura `yt-dlp` para que busque ese texto en YouTube, extraiga solo el audio (en formato mp3) y lo guarde en la ruta indicada.

### Fase 5: Unir todas las piezas (`src/main.py`)

1. Importa las funciones que creaste en los otros tres archivos.
2. Pide al usuario (usando `input()`) que introduzca el enlace de Spotify.
3. Ejecuta la función de Spotify para obtener los datos.
4. Ejecuta la función de carpetas para crear el directorio.
5. Haz un bucle (`for` loop) que recorra la lista de canciones y ejecute la función de descarga para cada una de ellas.

---

_Proyecto de uso estrictamente educativo._
