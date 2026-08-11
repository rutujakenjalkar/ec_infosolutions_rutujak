from celery import shared_task
from django.core.cache import cache
from .models import UserProfile, RecommendationLog
from .spotify import SpotifyService


@shared_task
def refresh_user_recommendations(user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        genres = user.favorite_genres if user.favorite_genres else ["pop"]
        
        # 1. Fetch from Spotify
        tracks = SpotifyService.get_recommendations(genres)
        
        # 2. Cache in Redis (Expires in 1 hour)
        cache_key = f"recommendations_{user_id}"
        cache.set(cache_key, tracks, timeout=3600)
        
        # 3. Log to Database
        RecommendationLog.objects.create(
            user=user,
            track_list=tracks
        )
        return f"Successfully refreshed for user {user_id}"
    except UserProfile.DoesNotExist:
        return f"User {user_id} not found"


@shared_task
def refresh_all_users_recommendations():
    """
    Periodic task triggered by Celery Beat to refresh recommendations for all users.
    """
    user_ids = UserProfile.objects.values_list('id', flat=True)
    for user_id in user_ids:
        refresh_user_recommendations.delay(user_id)
    return f"Enqueued recommendation refreshes for {len(user_ids)} users."