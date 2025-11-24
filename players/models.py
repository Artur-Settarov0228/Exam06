from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Players(models.Model):

    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=50)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname
    
    def update_rating(self, opponent_rating, result, k_factor=32):
        
        expected_score = 1 / (1 + 10 ** ((opponent_rating - self.rating) / 400))
        rating_change = k_factor * (result - expected_score)
        self.rating += round(rating_change)
        self.save()

    
    class Meta:
        ordering = ['-rating', 'nickname']

