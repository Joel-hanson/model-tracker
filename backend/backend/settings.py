import os
from pathlib import Path

from decouple import Csv, config


def base_dir_join(*args):
    return os.path.join(BASE_DIR, *args)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# debug configures the dev and production setup, False means the project runs in production mode and True means project runs in development mode.
DEBUG = config("DEBUG", default=False, cast=bool)

# Allowed hosts is the list of hosts to allow hitting the project.
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# The django apps and the external apps.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "celery",
    "rest_framework",
    "common",
    "registry",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [base_dir_join("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # },
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", default="postgres", cast=str),
        "USER": config("POSTGRES_USER", default="postgres", cast=str),
        "PASSWORD": config("POSTGRES_PASSWORD", default="postgres", cast=str),
        "HOST": config("POSTGRES_HOST", default="db", cast=str),
        "PORT": config("POSTGRES_PORT", default="5432", cast=str),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Redis
REDIS_URL = "redis://{host}:{port}/{db}".format(
    host=config("REDIS_HOST", "redis", cast=str),
    port=config("REDIS_PORT", "6379", cast=int),
    db=config("REDIS_DB", default=1, cast=int),
)

# Celery
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACKS_LATE = False
CELERY_TIMEZONE = TIME_ZONE

BROKER_URL = REDIS_URL
CELERY_BROKER_URL = REDIS_URL
CELERY_CACHE_BACKEND = "default"
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
# django setting caches using postgres.
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
CELERY_RESULT_PERSISTENT = True

# Storage
STATIC_ROOT = base_dir_join("staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = base_dir_join("mediafiles")
MEDIA_URL = "/media/"

# SSL
# SECURE_PROXY_SSL_HEADER = config('SECURE_PROXY_SSL_HEADER', cast=Csv(post_process=tuple))

# REST framework configuration.
REST_FRAMEWORK = {"TEST_REQUEST_DEFAULT_FORMAT": "json"}
