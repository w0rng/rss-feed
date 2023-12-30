from django.contrib import admin

from .models import Feed, Article, Read, Bookmark


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ("title", "articles_count", "views")

    def articles_count(self, obj):
        return obj.articles.count()

    def views(self, obj: Feed):
        return sum([a.count_read for a in obj.articles.all()])


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "count_read")


@admin.register(Read)
class ReadAdmin(admin.ModelAdmin):
    list_display = ("user", "article")


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "article")
