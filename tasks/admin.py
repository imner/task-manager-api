from django.contrib import admin
from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
