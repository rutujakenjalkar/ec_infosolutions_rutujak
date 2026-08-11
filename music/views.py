from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, views, status
from rest_framework.response import Response
from .models import UserProfile, UserActivity
from .serializers import UserProfileSerializer, UserActivitySerializer
from django.shortcuts import get_object_or_404


from rest_framework.views import APIView
from django.core.cache import cache
from .tasks import refresh_user_recommendations

from django.db.models import Count, Q
from .tasks import refresh_all_users_recommendations

# ViewSets are magical. This one small class automatically creates the logic for:
# - POST /users/ (Create a user)
# - GET /users/ (List all users)
# - GET /users/{id}/ (Get a specific user)
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# APIViews are for custom logic. We use this to explicitly handle incoming track interactions.
class UserActivityView(views.APIView):
    def post(self, request):
        serializer = UserActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RecommendationRefreshView(APIView):
    def post(self, request, user_id):

        user = get_object_or_404(UserProfile, id=user_id)
        # The .delay() method pushes this to Celery to run in the background
        refresh_user_recommendations.delay(user_id)
        return Response(
            {"message": "Recommendation refresh triggered asynchronously in the background."}, 
            status=status.HTTP_202_ACCEPTED
        )

class RecommendationListView(APIView):
    def get(self, request, user_id):

        if not UserProfile.objects.filter(id=user_id).exists():
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cache_key = f"recommendations_{user_id}"
        # Fetch directly from Redis memory
        tracks = cache.get(cache_key)
        
        # Check if key exists in Redis (even if tracks is an empty list [])
        if tracks is not None:
            return Response({"source": "redis_cache", "data": tracks}, status=status.HTTP_200_OK)
            
        return Response(
            {"message": "No cached recommendations found. Please trigger a refresh first."}, 
            status=status.HTTP_404_NOT_FOUND
        )




class UserActivityCreateView(APIView):
    def post(self, request):
        serializer = UserActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AnalyticsSummaryView(APIView):
    def get(self, request):
        stats = UserActivity.objects.aggregate(
            total_interactions=Count('id'),
            total_plays=Count('id', filter=Q(action='play')),
            total_likes=Count('id', filter=Q(action='like')),
            total_skips=Count('id', filter=Q(action='skip'))
        )
        return Response(stats)



class AnalyticsTrendsView(APIView):
    def get(self, request):
        # Group by genre and count occurrences, top 5
        top_genres = (
            UserActivity.objects.values('genre')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )

        # Group by artist_name and count occurrences, top 5
        top_artists = (
            UserActivity.objects.values('artist_name')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )

        return Response({
            "top_genres": list(top_genres),
            "top_artists": list(top_artists)
        }, status=status.HTTP_200_OK)



class UserAnalyticsView(APIView):
    def get(self, request, user_id):
        # 1. Verify user exists
        if not UserProfile.objects.filter(id=user_id).exists():
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Aggregate basic interaction stats
        stats = UserActivity.objects.filter(user_id=user_id).aggregate(
            total_interactions=Count('id'),
            total_plays=Count('id', filter=Q(action='play')),
            total_likes=Count('id', filter=Q(action='like')),
            total_skips=Count('id', filter=Q(action='skip'))
        )

        # 3. Calculate top genre for this user
        top_genre_data = (
            UserActivity.objects.filter(user_id=user_id)
            .values('genre')
            .annotate(count=Count('id'))
            .order_by('-count')
            .first()
        )
        stats['favorite_genre'] = top_genre_data['genre'] if top_genre_data else None

        # 4. Calculate top artist for this user
        top_artist_data = (
            UserActivity.objects.filter(user_id=user_id)
            .values('artist_name')
            .annotate(count=Count('id'))
            .order_by('-count')
            .first()
        )
        stats['favorite_artist'] = top_artist_data['artist_name'] if top_artist_data else None

        return Response(stats, status=status.HTTP_200_OK)


class RefreshRecommendationsView(APIView):
    def post(self, request, user_id):
        # Trigger Celery task in background (non-blocking)
        refresh_all_users_recommendations.delay(user_id)
        
        return Response(
            {
                "status": "success",
                "message": f"Recommendation refresh initiated for user {user_id} in the background."
            },
            status=status.HTTP_202_ACCEPTED
        )