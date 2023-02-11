from django.apps import AppConfig
import nltk
import os


class FeedConfig(AppConfig):
    name = 'apps.feed'
    verbose_name = 'feed'

    def ready(self):
        from django.db.models.signals import post_save
        from apps.feed.signals import my_handler
        from .models import Feed

        if not os.listdir("/root/nltk_data"):
            nltk.download('punkt')

        post_save.connect(my_handler, sender=Feed)
