from django.db import models

class Player(models.Model):
    nickname = models.CharField(max_length=100, unique=True)  
    country = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nickname