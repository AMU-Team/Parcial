# Usar una imagen oficial de Python como base
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc     

# Copiar el archivo de requerimientos
COPY ./requirements.txt /app/requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la API
COPY ./src /app/src

# Exponer el puerto que utilizará la API
EXPOSE 8000

# Comando para iniciar la API
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]