from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS para que el Frontend de Astro pueda pedirle cosas al Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"], # La ruta de Astro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "mensaje": "¡El Backend de Spotify está corriendo!"}