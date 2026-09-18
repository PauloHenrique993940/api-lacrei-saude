import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()


def required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"A variável de ambiente {name} é obrigatória.")
    return value


SECRET_KEY = required_env("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [host.strip() for host in required_env("ALLOWED_HOSTS").split(",") if host.strip()]
SECURE_ENVIRONMENT = ENVIRONMENT in {"staging", "production"}
SECURE_SSL_REDIRECT = SECURE_ENVIRONMENT
SECURE_HSTS_SECONDS = 31536000 if SECURE_ENVIRONMENT else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_ENVIRONMENT
SECURE_HSTS_PRELOAD = ENVIRONMENT == "production"
SESSION_COOKIE_SECURE = SECURE_ENVIRONMENT
CSRF_COOKIE_SECURE = SECURE_ENVIRONMENT

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.RequestLoggingMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

use_sqlite = os.getenv("USE_SQLITE", "False").lower() == "true"
if ENVIRONMENT in {"staging", "production"} and use_sqlite:
    raise RuntimeError("USE_SQLITE deve ser False em staging e produção.")

if use_sqlite:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": required_env("POSTGRES_DB"),
            "USER": required_env("POSTGRES_USER"),
            "PASSWORD": required_env("POSTGRES_PASSWORD"),
            "HOST": required_env("POSTGRES_HOST"),
            "PORT": required_env("POSTGRES_PORT"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["core.authentication.APIKeyAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["core.permissions.IsAuthenticatedWithAPIKey"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}

API_KEY = required_env("API_KEY")
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in required_env("CORS_ALLOWED_ORIGINS").split(",")
    if origin.strip()
]
CORS_ALLOW_CREDENTIALS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "standard"},
        "file": {
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "lacrei_api.log",
            "formatter": "standard",
        },
    },
    "loggers": {
        "core": {"handlers": ["console", "file"], "level": "INFO", "propagate": False},
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Lacrei Saúde API",
    "DESCRIPTION": "API REST para gerenciamento de profissionais e consultas médicas.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
