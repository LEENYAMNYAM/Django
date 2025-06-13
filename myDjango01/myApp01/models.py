from django.db import models

# Create your models here.

class Board(models.Model):
    idx = models.AutoField(primary_key=True) # Unique identifier for the board post
    writer = models.CharField(max_length=50, null=False) # Writer of the board post
    title = models.CharField(max_length=100, null=False) # Title of the board post
    content = models.TextField(null=False) # Title of the board post
    
    