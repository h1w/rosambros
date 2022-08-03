from django.db import models
from django.contrib.auth.models import User

MODERATION_LEVEL = (
  (0, "User"),
  (1, "Content Maker"),
  (2, "Moderator"),
  (3, "Administrator"),
)

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  description = models.TextField(blank=True, null=True)
  location = models.CharField(max_length=30, blank=True)
  date_joined = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  moderation_level = models.IntegerField(choices=MODERATION_LEVEL, default=0)

  class Meta:
    ordering = ['-date_joined']
  
  def __str__(self):
    return self.user.username
  
  def get_moderation_level(self):
    return self.moderation_level