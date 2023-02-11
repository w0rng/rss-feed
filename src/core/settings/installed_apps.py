from django.conf import settings

INSTALLED_APPS = [
    "django_dramatiq",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "django_filters",
    "apps.user",
    "apps.feed",
]

if settings.DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
