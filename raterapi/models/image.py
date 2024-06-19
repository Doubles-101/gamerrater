from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name="images")
    url = models.URLField()