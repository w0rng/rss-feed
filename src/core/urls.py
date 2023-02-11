from apps.feed import urls as feed_urls
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(("api.v1.urls", "api_v1"))),
    path("feed/", include((feed_urls, "feed"))),
]
