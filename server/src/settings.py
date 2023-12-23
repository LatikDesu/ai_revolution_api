import sys
from os import getenv, path
from pathlib import Path

import dotenv
from corsheaders.defaults import default_headers
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(__file__).parent.parent

sys.path.append(str(PROJECT_ROOT / 'apps'))

dotenv_file = BASE_DIR / '.env'

if path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DEVELOPMENT_MODE = getenv('DEVELOPMENT_MODE', 'False') == 'True'

APIKEY = getenv('OPENAI_APIKEY')
PROXY_URL = getenv('PROXY_URL')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('DJANGO_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DJANGO_DEBUG', False) == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

INSTALLED_APPS.extend(['users', 'prompts',
                      'conversations'])  # local apps
INSTALLED_APPS.extend(['corsheaders', 'rest_framework', 'drf_yasg', 'djoser',
                      'social_django'])  # installed apps

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, 'templates')],
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

# Domain names
DOMAIN = getenv('DOMAIN')
SITE_NAME = 'DEEPLINE'
SITE_ID = int(getenv('SITE_ID', 1))
SITE_URL = getenv('SITE_URL', 'https://deep-line.ru')

WSGI_APPLICATION = 'src.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": getenv("SQL_ENGINE", "django.db.backends.postgresql_psycopg2"),
            "NAME": getenv("SQL_DATABASE", "ai_db"),
            "USER": getenv("SQL_USER", "postgres"),
            "PASSWORD": getenv("SQL_PASSWORD", "postgres"),
            "HOST": getenv("SQL_HOST", "db"),
            "PORT": getenv("SQL_PORT", "5432"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Config
CORS_ALLOWED_ORIGINS = getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://127.0.0.1:8100,http://localhost:8100'
).split(',')
CORS_ALLOW_CREDENTIALS = True


# REST_FRAMEWORK Config
REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S.%fZ',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.CustomJWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {'anon': '100/second', 'user': '1000/second', 'subscribe': '60/minute'},
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
}

# DJOSER Config
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activation/{uid}/{token}',
    # 'USER_CREATE_PASSWORD_RETYPE': True,
    # 'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': getenv('REDIRECT_URLS').split(','),
    'SERIALIZERS': {
        'current_user': 'users.serializers.CustomUserSerializer',
    }
}

# Sending emails
DEFAULT_FROM_EMAIL = getenv('DEFAULT_FROM_EMAIL')
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_PORT = getenv('EMAIL_PORT')
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = False


# Authentication
AUTH_COOKIE = 'access'
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24
AUTH_COOKIE_SECURE = getenv('AUTH_COOKIE_SECURE', 'True') == 'True'
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE = 'None'

AUTH_USER_MODEL = 'users.UserAccount'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]


# Social Authentication
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = getenv('GOOGLE_AUTH_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = getenv('GOOGLE_AUTH_SECRET_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']

SOCIAL_AUTH_VK_OAUTH2_KEY = getenv('VK_AUTH_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = getenv('VK_AUTH_SECRET_KEY')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_GITHUB_KEY = getenv('GH_AUTH_KEY')
SOCIAL_AUTH_GITHUB_SECRET = getenv('GH_AUTH_SECRET_KEY')
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']


CSRF_COOKIE_SECURE = bool(getenv('CSRF_COOKIE_SECURE', True))
SESSION_COOKIE_SECURE = bool(getenv('SESSION_COOKIE_SECURE', True))

# # False since we will grab it via universal-cookies
CSRF_COOKIE_HTTPONLY = bool(getenv('CSRF_COOKIE_HTTPONLY', False))

SESSION_COOKIE_HTTPONLY = bool(getenv('SESSION_COOKIE_HTTPONLY', True))
SESSION_COOKIE_SAMESITE = getenv('SESSION_COOKIE_SAMESITE', "None")
CSRF_COOKIE_SAMESITE = getenv('CSRF_COOKIE_SAMESITE', "None")
CORS_ALLOW_CREDENTIALS = bool(getenv('CORS_ALLOW_CREDENTIALS', True))
CORS_ORIGIN_ALLOW_ALL = bool(getenv('CORS_ORIGIN_ALLOW_ALL', True))
CSRF_COOKIE_NAME = getenv('CSRF_COOKIE_NAME', "csrftoken")
CSRF_TRUSTED_ORIGIN = getenv('CSRF_TRUSTED_ORIGINS', "localhost:3000")
CSRF_TRUSTED_ORIGIN = CSRF_TRUSTED_ORIGIN.split(',')
CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGIN

CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-CSRFToken', 'Accept',
]
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']

X_FRAME_OPTIONS = getenv('X_FRAME_OPTIONS', 'DENY')
SECURE_BROWSER_XSS_FILTER = bool(getenv('SECURE_BROWSER_XSS_FILTER', True))

# Headers
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
