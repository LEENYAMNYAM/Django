from django.db import models

# Create your models here.

class Movie(models.Model):
    rank = models.CharField(null = True, max_length = 20)
    title = models.CharField(null = True, max_length = 500)
    grade = models.CharField(null = True, max_length = 20)
    custom_count = models.CharField(null = True, max_length = 200)