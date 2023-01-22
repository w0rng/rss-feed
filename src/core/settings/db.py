from core.settings import env

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/db/db.sqlite3",
    },
}
