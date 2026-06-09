from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'rank', 'exp', 'aura')
    list_filter = ('rank', 'level')
    search_fields = ('user__email', 'user__name')
