from django.db import models

# Create your models here.
class PopularCocktail(models.Model):
    cocktail_id = models.CharField(max_length=50, unique = True, null = True, blank = True)
    name = models.CharField(max_length=200, unique=True)
    search_count = models.PositiveIntegerField(default=0)
    alcoholic = models.CharField(max_length=50, blank = True, null = True)
    image = models.URLField(blank = True, null = True)
    instructions = models.TextField(blank = True, null = True)
    ingredients = models.JSONField(blank = True, null = True)
    def __str__(self):
        return f"{self.name} ({self.search_count})"