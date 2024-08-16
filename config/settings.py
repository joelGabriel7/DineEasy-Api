import os
from pathlib import Path

from config import db

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c##j$oyfz3q-mn1u-k@!3%bt83-&reb^!m5)nw#3g=d(i_i81&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #thirdy packeges
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'django_filters',
    #apps
    'core.restaurant',
    "core.customers",
    "core.reservations"

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = db.SQLITE
DATABASES = db.POSTGRESQL


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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'

# AUTH_USER_MODEL
AUTH_USER_MODEL = 'customers.CustomerUser'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 5
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# SPECTACULAR_SETTINGS = {
#     'TITLE': 'DineEasy API',
#     'DESCRIPTION': 'API para la automatización de reservas en restaurantes',
#     'VERSION': '1.0.0',
#     'SERVE_INCLUDE_SCHEMA': False,
# }

SPECTACULAR_SETTINGS = {
    'TITLE': 'DineEasy API',
    'DESCRIPTION': 'API para la automatización de reservas en restaurantes',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'TAGS': [
        {'name': 'Restaurantes', 'description': 'Operaciones relacionadas con restaurantes'},
        {'name': 'Mesas', 'description': 'Operaciones relacionadas el manejo de las mesas para los restaurantes'},
        {'name': 'Customers', 'description': 'Operaciones relacionadas el manejo de clientes para los restaurantes'},
        # Añade más tags según sea necesario
    ],
    'CONTACT': {
        'name': 'Equipo de Soporte DineEasy',
        'email': 'support@dineeasy.com',
        'url': 'https://www.dineeasy.com/support',
    },
    'LICENSE': {
        'name': 'BSD License',
        'url': 'https://opensource.org/licenses/BSD-3-Clause',
    },
    'EXTENSIONS_INFO': {
        'x-logo': {
            'url': 'https://www.example.com/logo.png',
            'backgroundColor': '#FFFFFF',
            'altText': 'DineEasy logo'
        },
    },
}