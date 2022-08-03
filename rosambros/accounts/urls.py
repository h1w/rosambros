from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserProfileListCreateView, UserProfileDetailView

urlpatterns = [
  path('all-profiles/', UserProfileListCreateView.as_view(), name='all-profiles'), # gets all user profiles and create a new profile
  path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile'), # retrieves profile details of the currently logged in user
]