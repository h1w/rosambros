from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
  user=serializers.StringRelatedField(read_only=True)
  first_name = serializers.SerializerMethodField(read_only=True)
  last_name = serializers.SerializerMethodField(read_only=True)
  email = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model=UserProfile
    fields = (
      'id',
      'user',
      'first_name',
      'last_name',
      'email',
      'description',
      'date_joined',
    )
  
  def get_first_name(self, obj):
    return obj.user.first_name
  
  def get_last_name(self, obj):
    return obj.user.last_name
  
  def get_email(self, obj):
    return obj.user.email

class UserProfileForListSerializer(serializers.ModelSerializer):
  user=serializers.StringRelatedField(read_only=True)
  email = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model=UserProfile
    fields=('id', 'user', 'email', 'date_joined',)
  
  def get_email(self, obj):
    return obj.user.email