from core.settings.environ import env
from split_settings.tools import include

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)


include(
    "boilerplate.py",
    "db.py",
    "installed_apps.py",
    "locale.py",
    "middleware.py",
    "drf.py",
    "sentry.py",
    "static.py",
    "media.py",
    "templates.py",
    "auth.py",
    "dramatiq.py",
)
