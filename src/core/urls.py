from django.contrib import admin
from django.urls import path

from feed.views import FeedView, ArticleDetailView, SaveDetailView, ArticleVeiwedView, BookmarksView, RssView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", FeedView.as_view(), name="home"),
    path("bookmarks", BookmarksView.as_view(), name="bookmarks"),
    path("article/<int:pk>", ArticleDetailView.as_view(), name="article_detail"),
    path("article/<int:pk>/save", SaveDetailView.as_view(), name="article_save"),
    path("article/<int:pk>/read", ArticleVeiwedView.as_view(), name="article_read"),
    path("rss/", RssView(), name="rss")
]
