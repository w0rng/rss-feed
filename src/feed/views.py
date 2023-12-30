from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView

from .models import Article, Read, Bookmark


class FeedView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user_id
        context["articles"] = (
            Article.objects.exclude(reads__user=user).order_by("-created_at").values_list("id", flat=True)[:100]
        )
        return context


class BookmarksView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user_id
        context["articles"] = (
            Article.objects.filter(bookmarks__user=user).order_by("-created_at").values_list("id", flat=True)
        )
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article.html"

    def get_object(self, queryset=None):
        user = self.request.user_id
        object = super().get_object(queryset)
        object.saved = object.bookmarks.filter(user=user).exists()
        return object


class SaveDetailView(ArticleDetailView):
    model = Article
    template_name = "article.html"

    def post(self, request, *args, **kwargs):
        user = self.request.user_id
        article = self.get_object()
        bookmark, created = Bookmark.objects.get_or_create(user=user, article=article)
        if not created:
            bookmark.delete()
        return HttpResponseRedirect(reverse("article_detail", args=(article.pk,)))


class ArticleVeiwedView(DetailView):
    model = Article

    def get(self, request, *args, **kwargs):
        user = self.request.user_id
        article = self.get_object()
        Read.objects.get_or_create(user=user, article=article)
        return HttpResponseRedirect(reverse("article_detail", args=(article.pk,)))
