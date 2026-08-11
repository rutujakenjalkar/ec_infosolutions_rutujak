from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, RecommendationLog, UserActivity

# Register your models here so they appear in the admin panel
admin.site.register(UserProfile)
admin.site.register(RecommendationLog)
admin.site.register(UserActivity)