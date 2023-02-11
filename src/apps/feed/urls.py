from django.urls import path

from .views import feed

urlpatterns = [
    path("<username>/", feed, name="feed"),
]
