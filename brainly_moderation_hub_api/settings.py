import os
import environ
from pathlib import Path
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env()
environ.Env.read_env(BASE_DIR / f".env.{os.environ.get('DJANGO_ENV', 'development')}")


DEBUG = env.bool("DEBUG")
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1"]

WSGI_APPLICATION = "brainly_moderation_hub_api.wsgi.application"
ROOT_URLCONF = "brainly_moderation_hub_api.urls"

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ["authorization", "content-type", "x-requested-with"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware"
]

if DEBUG:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


# Tenplates and static files

STATIC_URL = "static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# Databases

DATABASES = {
    "default": {
        "ENGINE": "timescale.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "QUOTED_LITERAL": "double"
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
    ("uk", _("Ukrainian")),
]

LOCALE_PATHS = [BASE_DIR / "locale/"]

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
