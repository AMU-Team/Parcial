# Importar la función create_engine de SQLAlchemy para crear el motor de base de datos
from sqlalchemy import create_engine
# Importar sessionmaker de SQLAlchemy para crear una fábrica de sesiones
from sqlalchemy.orm import sessionmaker
# Importar el módulo os para acceder a variables de entorno
import os

# Obtener la variable de entorno DOCKER_ENV, por defecto es "False"
docker_env = os.getenv("DOCKER_ENV", "False")

# URL de conexión a la base de datos PostgreSQL (ajustar según sea necesario)
# Si la aplicación está corriendo en un entorno Docker, usar la URL de conexión para Docker
if os.getenv("DOCKER_ENV") == "True":
    DATABASE_URL = "postgresql://user:password@db:5432/car_race"
# Si la aplicación no está en Docker, usar la URL de conexión local
else:
    DATABASE_URL = "postgresql://user:password@localhost:5432/car_race"
    
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener una sesión de base de datos en las rutas
# Esta función es un generador que proporciona una sesión de base de datos y la cierra automáticamente
def get_db():
    # Crear una nueva sesión de base de datos
    db = SessionLocal()
    try:
        # Devolver la sesión de base de datos
        yield db
    finally:
        # Cerrar la sesión de base de datos al finalizar
        db.close()