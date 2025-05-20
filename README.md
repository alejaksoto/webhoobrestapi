# Pasos para la instalación de python-django local
1. Instación de ambiente virtual python
python -r venv env
2. activación de ambiente virtual
\env\Scripts> .\activate
3. Instalación de la versión de Django
pip install django djangorestframework django-cors-headers
4. creación de proyecto django
django-admin startproject proyecto_django
5. Ingreso a la carpeta del proyecto
cd .\proyecto_django\
python manage.py startapp inicio
6. ejecutar el proyecto , validando su instalación
python manage.py runserver
--se debe ejecutar este comando para actualizar los archivos staticos en el general
python manage.py collectstatic
-- se debe ejecutar este comando cuando se realice modificaciones dentro de settings
python manage.py migrate
--comando para ver los paquetes instalados
py -m pip freeze
pip freeze > requirements.txt
--comando para instalar los paquetes necesarios
pip install -r requirements.txt
instalación de mariadb: C:\Program Files\MariaDB 11.7\bin>
--Comando para la imagen en docker
docker build -t dockerfile .
--comando para tagear la imagen
docker tag dockerfile alejaksoto/dockerfile:latest
--comando para hacer el cargue a docker hub
docker push alejaksoto/dockerfile:latest
--comando para ver los resultados del despliegue en la web app de azure
az webapp log tail --name meta09 --resource-group "pruebas-ai-implementacion"