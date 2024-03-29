import random
from collections import defaultdict
from itertools import chain

from django.contrib.syndication.views import Feed as RSSFeedView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView

from .models import Article, Read, Bookmark, Feed


class FeedView(TemplateView):
    template_name = "index.html"
    MAX_ARTICLES = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["articles"] = self.articles()

        return context

    def articles(self):
        user = self.request.user_id
        articles = Article.objects.exclude(reads__user=user).order_by("-created_at").prefetch_related("feed")

        articles_by_feed = defaultdict(list)
        max_count_per_feed = self.MAX_ARTICLES // (Feed.objects.count() or 1)

        for article in articles:
            if article.is_bad:
                continue
            if len(articles_by_feed[article.feed.pk]) >= max_count_per_feed:
                continue
            articles_by_feed[article.feed.pk].append(article.pk)

        result = list(chain.from_iterable(articles_by_feed.values()))
        random.shuffle(result)
        return result[: self.MAX_ARTICLES]


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


class RssView(RSSFeedView):
    title = "w0rng feed"
    link = "/rss/"
    description = "w0rng feed"
    limit = 20

    def items(self):
        return Article.objects.order_by("-created_at")[: self.limit]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return "\n".join(item.paragraphs)

    def item_link(self, item):
        return item.url
