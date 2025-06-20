from pathlib import Path
import os
import logging
import ssl

AUTH_USER_MODEL = 'inicio.Usuario'
USERNAME_FIELD = 'username'
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3wo00@h6^f=s_tbu1h-fjiy#-81=8ni)^^x+-+0ovbzevpi9q3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']
Token_Whatsapp= 'EAALuSgfSXl0BO3ZAZCKDixluR32bIlkV6jG0rAvKlLymDzFLxbBIjnuriTQicuAcgnFPqWIccZCzaPuxyFztMKt4uD2tDz9BGJEv5kwfS5iZAzrkPsESoR9a8m5FE7itEOZCNGSJxePEASToye4UvcBumzpWHUJAYPLWYiq8Ig6WTU2gggyf6i6JGHtsTB8ZCVTu1ZALudyXjxnLaK5AEj22JxNZCZCZA8iLCr0pU4yPuZB'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'inicio',
    'campanias',
    'empresas',
    'webhooks',
    'drf_yasg'
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',]
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # si tu frontend está ahí
    "http://127.0.0.1:3000",
]

ROOT_URLCONF = 'proyecto_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proyecto_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
print("Ruta del certificado SSL usada:", os.path.join(BASE_DIR, 'certs', 'BaltimoreCyberTrustRoot.crt.pem'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'solucionmeta-database',
        'USER': 'cpplasidso',
        'PASSWORD': 'Claro2025*',
        'HOST': 'solucionmeta-server.mysql.database.azure.com',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'ssl': {
                'ca': os.path.join(BASE_DIR, 'certs', 'DigiCertGlobalRootCA.crt.pem'),
                'cert_reqs': ssl.CERT_REQUIRED
            },   
    }
}}
ca_path = os.path.join(BASE_DIR, 'certs', 'DigiCertGlobalRootCA.crt.pem')
if not os.path.exists(ca_path):
    raise FileNotFoundError(f"Certificado no encontrado en: {ca_path}")



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'inicio/templates/inicio/static')]
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'inicio', 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Verificar STATICFILES_DIRS
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"STATICFILES_DIRS: {STATICFILES_DIRS}")

# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
