from django.db import models
from django.contrib.auth.models import User

class Show(models.Model):
    title = models.CharField(max_length=255)
    duration = models.IntegerField()  # Duration in minutes
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watched_date = models.DateField(auto_now_add=True)  # Date when the show was watched
    is_favorite = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration = models.IntegerField()  # Duration in minutes
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watched_date = models.DateField(auto_now_add=True)  # Date when the movie was watched
    is_favorite = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class ToWatchShow(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ToWatchMovie(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title