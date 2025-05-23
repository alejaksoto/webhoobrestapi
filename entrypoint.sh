#!/bin/sh

# Esperar a que la base de datos esté disponible (opcional si usas contenedor para DB)
# echo "Esperando la base de datos..."
# sleep 10

echo "Aplicando migraciones..."
python manage.py migrate

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Creando superusuario si no existe..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='mayra.soto').exists():
    User.objects.create_superuser('mayra.soto', 'mayra.soto', 'Claro2025*')
EOF

echo "Levantando el servidor con Gunicorn..."
exec gunicorn proyecto_django.wsgi:application --bind 0.0.0.0:8000
