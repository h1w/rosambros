from django.shortcuts import get_object_or_404
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import UserProfile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer, UserProfileForListSerializer

class UserProfileListCreateView(ListCreateAPIView):
  queryset=UserProfile.objects.all()
  serializer_class=UserProfileForListSerializer
  permission_classes=[IsAuthenticated]

  def perform_create(self, serializer):
    user=self.request.user
    serializer.save(user=user)

class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
  queryset=UserProfile.objects.all()
  serializer_class=UserProfileSerializer
  permission_classes=[IsOwnerProfileOrReadOnly, IsAuthenticated]

class UserHasAdminPermissions(APIView):
  def get(self, request, format=None):
    if request.user.is_authenticated:
      user_profile = get_object_or_404(UserProfile, user=request.user)
      if user_profile.moderation_level >= 3:
        return Response({'isadmin': True}, status=status.HTTP_200_OK)
      else:
        return Response({'isadmin': False}, status=status.HTTP_200_OK)
    else:
      return Response({'isadmin': False}, status=status.HTTP_200_OK)