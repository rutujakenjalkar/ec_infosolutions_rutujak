from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnalyticsSummaryView,
    AnalyticsTrendsView,
    RecommendationListView,
    RecommendationRefreshView,
    UserActivityCreateView,
    UserActivityView,
    UserAnalyticsView,
    UserProfileViewSet,
)



# DefaultRouter automatically generates the standard URLs for our magical ViewSet
router = DefaultRouter()
router.register(r'users', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('activity/', UserActivityView.as_view(), name='user-activity'),
    path('recommendations/<int:user_id>/refresh/', RecommendationRefreshView.as_view(), name='refresh-recommendations'),
    path('recommendations/<int:user_id>/', RecommendationListView.as_view(), name='list-recommendations'),
    path('activity/', UserActivityCreateView.as_view(), name='activity-create'),
    path('analytics/summary/', AnalyticsSummaryView.as_view(), name='analytics-summary'),
    path('analytics/trends/', AnalyticsTrendsView.as_view(), name='analytics-trends'),
    path('analytics/user/<int:user_id>/', UserAnalyticsView.as_view(), name='user-analytics')
    
]