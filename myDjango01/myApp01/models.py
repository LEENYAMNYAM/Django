from django.db import models
from datetime import datetime

# Create your models here.

class Board(models.Model):
    idx = models.AutoField(primary_key=True) # Unique identifier for the board post
    writer = models.CharField(max_length=50, null=False) # Writer of the board post
    title = models.CharField(max_length=100, null=False) # Title of the board post
    content = models.TextField(null=False) # Title of the board post
    hit = models.IntegerField(default=0)
    post_date = models.DateField(default=datetime.now, blank=True)
    filename = models.CharField(null=True, blank=True, default='', max_length=500)
    filesize = models.IntegerField(default=0)
    down = models.IntegerField(default=0)

    def hit_up(self):
        self.hit +=1

    def down_up(self):
        self.down +=1

class Comment(models.Model):
    idx = models.AutoField(primary_key=True)
    board_idx = models.IntegerField(null=False)
    writer = models.CharField(null=False, max_length=50)
    content = models.TextField(null=False)
    post_date = models.DateTimeField(default=datetime.now, blank=True)
    