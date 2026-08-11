from rest_framework import serializers
from .models import UserProfile, RecommendationLog, UserActivity

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__' 

class RecommendationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationLog
        fields = '__all__'

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'



class UserActivitySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(), 
        source='user'
    )

    class Meta:
        model = UserActivity
        fields = ['id', 'user_id', 'track_name', 'artist_name', 'action', 'timestamp']
        read_only_fields = ['id', 'timestamp']