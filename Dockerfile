# Usa la imagen oficial de Python
FROM python:3.13-alpine


# Instala dependencias del sistema
RUN apk add --no-cache \
    mariadb-connector-c \
    mariadb-dev \
    gcc \
    musl-dev \
    python3-dev

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo los archivos necesarios primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto
COPY . .

# Exponer el puerto de la aplicación


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
# Ejecutar migraciones y levantar el servidor con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "proyecto_django.wsgi:application"]

