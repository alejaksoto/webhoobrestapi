#!/bin/sh
echo "Esperando a que la base de datos esté lista..."
while ! nc -z db 3306; do
  sleep 1
done

echo "Aplicando migraciones..."
python manage.py migrate

echo "Creando superusuario si no existe..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'mayra.soto@claro.com.co', 'Claro2025*')"

echo "Levantando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 proyecto_django.wsgi:application
