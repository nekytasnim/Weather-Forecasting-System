from turtle import title
from django.db import models

class Create(models.Model):
    title = models.CharField(max_length=10)

class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="media")
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title