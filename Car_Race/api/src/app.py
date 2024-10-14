from fastapi import FastAPI, Response  # Importar FastAPI y Response de fastapi
from src.database_connection import engine  # Importar el motor de conexión a la base de datos
from src.models import Base  # Importar la base de los modelos de la base de datos
from src.routes import router as game_router  # Importar el enrutador de rutas del juego
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST  # Importar funciones para métricas de Prometheus

# Crear la base de datos y las tablas
Base.metadata.drop_all(bind=engine)  # Eliminar las tablas actuales si existen
Base.metadata.create_all(bind=engine)  # Crear las tablas de nuevo basadas en los modelos

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Cars Race Game",  # Título de la aplicación
    description="Un juego de carrera de coches donde los jugadores compiten",  # Descripción de la aplicación
    version="1.0.0"  # Versión de la aplicación
)

# Incluir las rutas del juego
app.include_router(game_router)  # Agregar las rutas definidas en el enrutador del juego

# Root endpoint para verificar si la API está en funcionamiento
@app.get("/")
def read_root():
    return {"message": "Welcome to the Cars Race Game API!"}

# Endpoint para las métricas
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)