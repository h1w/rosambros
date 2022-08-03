from django.contrib import admin
from .models import Marker

class MarkerAdmin(admin.ModelAdmin):
  list_display = ('street', 'name', 'description', 'gps', 'status', 'deletion_author', 'created_on',)
  list_filter = ('created_on', 'status',)
  search_filter = ('street', 'name', 'description', 'gps', 'deletion_author', 'created_on',)

admin.site.register(Marker, MarkerAdmin)

admin.site.site_header="Marker"