from django.core.validators import MinValueValidator

from apps.user.models import User
from django.db import models


class Feed(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    last_update = models.DateField(editable=False, auto_now_add=True)
    interval = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(600)],
        help_text="in sec",
        default=600,
    )

    def __str__(self):
        return self.title
