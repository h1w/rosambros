from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import UserProfile

class IsOwnerProfileOrReadOnly(BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in SAFE_METHODS:
      return True
    return obj.user==request.user

class IsOwnerProfileWithLevelModer(BasePermission):
  def has_permission(self, request, view):
    if UserProfile.objects.get(user=request.user).moderation_level >= 2:
      print('TRUE TRUE TRUE TRUE ABOBA')
      print(request.user)
      print(UserProfile.objects.get(user=request.user).moderation_level)
    return (UserProfile.objects.get(user=request.user).moderation_level >= 2)

class IsOwnerProfileWithLevelAdministrator(BasePermission):
  def has_permission(self, request, view):
    return (UserProfile.objects.get(user=request.user).moderation_level >= 3)
