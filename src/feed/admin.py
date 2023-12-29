from django.contrib import admin

from .models import Feed, Article, Read, Bookmark


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "count_read")


@admin.register(Read)
class ReadAdmin(admin.ModelAdmin):
    pass


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass
