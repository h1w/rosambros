from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'description', 'location', 'moderation_level', 'date_joined', 'updated_on',)
  list_filter = ('location', 'date_joined', 'moderation_level', 'updated_on',)
  search_filter = ('user', 'description', 'location', 'moderation_level',)

admin.site.register(UserProfile, UserProfileAdmin)

admin.site.site_header="UserProfile"