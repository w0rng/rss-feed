from .tasks import load_new_posts


def my_handler(sender, instance, created, **kwargs):
    # if not created:
    #     return
    load_new_posts.send(instance.pk)
