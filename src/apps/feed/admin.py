from django.contrib import admin

from .models import Feed, Post


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ("title", "url")

    def get_queryset(self, request):
        user = request.user
        return super().get_queryset(request).filter(author=user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "get_tags", "feed", "published")
    ordering = ("-published",)

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    get_tags.short_description = "Tags"

    def get_queryset(self, request):
        user = request.user
        return super().get_queryset(request).filter(feed__author=user)
