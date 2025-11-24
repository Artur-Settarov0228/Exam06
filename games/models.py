from django.db import models
from django.core.exceptions import  ValidationError

# Create your models here.

class Game(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=650)
    start_date  = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.score_set.exists():
            raise ValidationError(
                 "Ushbu turnirga bog'liq natijalar mavjud. "
                "Avval bog'liq natijalarni o'chiring."
            )
        super().delete(*args, **kwargs)
    

