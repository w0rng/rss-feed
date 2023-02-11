from apps.feed.service.generate_feed import FeedGenerator
from apps.user.models import User
from django.http import HttpResponse


def feed(request, username):
    user = User.objects.get(username=username)
    generator = FeedGenerator(user)
    return HttpResponse(generator.generate(), content_type="application/rss+xml")
