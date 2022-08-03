from django.dispatch import receiver
import os
from .models import Marker
from django.db.models.signals import post_delete

@receiver(post_delete, sender=Marker)
def auto_delete_photo_on_delete(sender, instance, **kwargs):
  if instance.image:
    if os.path.isfile(instance.image.path):
      os.remove(instance.image.path)