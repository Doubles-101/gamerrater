from django.db import models
from django.contrib.auth.models import User



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name="reviews")
    comment = models.CharField(max_length=(10000))
    