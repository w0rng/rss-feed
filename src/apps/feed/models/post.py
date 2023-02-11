from django.db import models
from .feed import Feed
from .tag import Tag


class Post(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    published = models.DateTimeField()
    short_post = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
