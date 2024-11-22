from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "::1"]

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = False

SECURE_HSTS_PRELOAD = False

SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
