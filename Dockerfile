# Usa la imagen oficial de Python
FROM python:3.13-alpine


# Instala dependencias del sistema
RUN apk add --no-cache \
    mariadb-connector-c \
    mariadb-dev \
    gcc \
    musl-dev \
    python3-dev \
    bash \
    netcat-openbsd  

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo los archivos necesarios primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]


EXPOSE 8000

# Ejecutar migraciones y levantar el servidor con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "proyecto_django.wsgi:application"]

