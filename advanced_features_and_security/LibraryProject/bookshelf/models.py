from django.db import models
from django.conf import settings  # ✅ use the custom user model

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # new field

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
