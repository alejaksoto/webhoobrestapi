# Usa la imagen oficial de Python
FROM python:3.10

# Instala dependencias del sistema
RUN apt update && apt install -y \
    libmariadb3 \
    libmariadb-dev-compat \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo los archivos necesarios primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto
COPY . .

# Exponer el puerto de la aplicación
EXPOSE 8000

# Ejecutar migraciones y levantar el servidor con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "proyecto_django.wsgi:application"]
