from django.apps import AppConfig


class FeedConfig(AppConfig):
    name = 'apps.feed'
    verbose_name = 'feed'

    def ready(self):
        import nltk
        nltk.download('punkt')
        from django.db.models.signals import post_save
        from apps.feed.signals import my_handler
        from .models import Feed

        post_save.connect(my_handler, sender=Feed)
