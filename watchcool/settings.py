"""
Django settings for watchcool project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import socket
from django.contrib.messages import constants as message_constants
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MESSAGE_LEVEL = message_constants.INFO
# APPEND_SLASH = False
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v1g$)!1p9)ksqngz^ro_a=5(b_j^@ps%(odf(w5u3#84y!k4&n'
# SECURITY WARNING: don't run with debug turned on in production!

if socket.gethostname() == 'dynasty':
    DEBUG = False
    # PREPEND_WWW=True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    DEBUG = True
ALLOWED_HOSTS = [".watchcool.in","localhost","127.0.0.1","172.16.0.218",]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "webapp.apps.WebappConfig",
    "adminDashboard.apps.AdmindashboardConfig",
    "appapi.apps.AppapiConfig",
    "rest_framework",
    'django.contrib.sitemaps',
]

MIDDLEWARE = [
    'webapp.virtualhostmiddleware.VirtualHostMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'watchcool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates",],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webapp.context_processors.config',
            ],
            "libraries":{
                "classname":"adminDashboard.templatetags.classname",
            }
        },
    },
]

WSGI_APPLICATION = 'watchcool.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'watchcool_webapp',
            'HOST':'localhost',
            'USER':'cooluser',
            'PASSWORD':'Imcooluser@2021',
            'PORT':3306,
            'OPTION': {'init_command':"SET sql_mode='STRICT_TRANS_TABLE',"},

        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3'

        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
#cache
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.db.DatabaseCache',
        'LOCATION':'cache',
        'OPTIONS':{
            "MAX_ENTRIES":8000,
        },
    }
}
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'appapi.handlers.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': [
        'appapi.permissions.ReadOnly',
    ]

}
STATIC_URL = '/static/'
MEDIA_URL = '/externalmedia/'
if not DEBUG:
    STATIC_ROOT = "/var/www/html/static.watchcool.in"
    MEDIA_ROOT = "/var/www/html/media.watchcool.in"
else:
    STATIC_ROOT = BASE_DIR/"assets"
    MEDIA_ROOT = BASE_DIR/"media"
AUTH_USER_MODEL  = "webapp.CustomUser"
AUTHENTICATION_BACKENDS = ["webapp.backends.EmailBackend",]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
CACHE_TIME = 60*60*3
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = "app_webapp:login"
LOGIN_REDIRECT_URL = "app_webapp:home"
LOGOUT_REDIRECT_URL = "app_webapp:home"