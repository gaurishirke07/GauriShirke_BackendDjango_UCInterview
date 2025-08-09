from django.db import models

# Create your models here.
class PopularCocktail(models.Model):
    name = models.CharField(max_length=200, unique=True)
    search_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.search_count})"