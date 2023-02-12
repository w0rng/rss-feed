from core.settings import env

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": "5432",
        "CONN_MAX_AGE": 300,
    },
}
