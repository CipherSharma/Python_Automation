from django.db import models

class Blogs(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    url = models.URLField()
