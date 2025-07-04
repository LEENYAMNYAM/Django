from django.db import models

# Create your models here.

class Movie(models.Model):
    rank = models.CharField(null = True,max_length=20)
    title = models.CharField(null = True,max_length=700)
    grade = models.FloatField(null = True)
    custom_count = models.CharField(null = True,max_length=500)
