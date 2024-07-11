from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_created")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    designer = models.CharField(max_length=100)
    year_released = models.IntegerField(validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ])
    number_of_players = models.IntegerField(validators=[
            MinValueValidator(0),
            MaxValueValidator(1000000000)
        ])
    estimated_time_to_play = models.TimeField()
    age_recommendation = models.IntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(120)
        ])
    
    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = self.ratings.all()

        if not ratings:
            return 0

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating_number

        # Calculate the average and return it.
        average = total_rating / len(ratings)

        return average
        #return the result
