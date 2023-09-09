# Imagen base
FROM python:3.9-alpine



# Copiar los archivos necesarios
COPY .env .env
COPY requirements.txt .

# Instalar las dependencias
RUN python -m pip install --upgrade pip
RUN apk update && apk add mariadb-connector-c-dev build-base mysql-dev && pip install -r requirements.txt
RUN apk add curl

# Directorio de trabajo de la aplicación
WORKDIR /app
COPY app /app

# Comando para iniciar la aplicación
CMD ["python", "run.py"]