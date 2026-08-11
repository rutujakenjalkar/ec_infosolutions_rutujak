
# Create your models here.

from django.db import models
from django.db import models


class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
    # Store user preferences as JSON lists, e.g., ["pop", "rock"]
    favorite_genres = models.JSONField(default=list, blank=True)
    favorite_artists = models.JSONField(default=list, blank=True)
    favorite_moods = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class RecommendationLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='recommendation_logs')
    
    # Keeps a permanent historical log of tracks recommended by Spotify
    track_list = models.JSONField(default=list)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendations for {self.user.email} at {self.timestamp}"


class UserActivity(models.Model):

    ACTION_CHOICES = [
        ('play', 'Play'),
        ('like', 'Like'),
        ('skip', 'Skip'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='activities')
    track_id = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.action} - {self.track_name}"