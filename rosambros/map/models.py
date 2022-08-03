from django.db import models
from rosambros.settings import DOMAIN_PORT
import requests
import json
from accounts.models import UserProfile

STATUS = (
  (0, "Draft"),
  (1, "Posted"),
  (2, "Archived"),
)

class Marker(models.Model):
  name = models.CharField(max_length=200, blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  gps = models.CharField(max_length=200)
  image = models.ImageField(upload_to='uploads/',  blank=True, null=True)
  created_on = models.DateTimeField(auto_now_add=True)
  street = models.TextField(blank=True, null=True)
  status = models.IntegerField(choices=STATUS, default=1)
  deletion_author = models.ForeignKey(UserProfile, on_delete=models.RESTRICT, related_name='deletion_author', null=True, blank=True)
  deletion_datetime = models.DateTimeField(blank=True, null=True)

  class Meta:
    ordering = ('-created_on',)
  
  def __str__(self):
    return f'{self.id}_{self.name}'
    
  def save(self, *args, **kwargs):
    try:
      response = requests.get(f'''https://nominatim.openstreetmap.org/reverse?lat={self.gps.split(',')[0].strip(' ')}&lon={self.gps.split(',')[1].strip(' ')}&format=json''')

      jsn = json.loads(response.content.decode())
      s = str(jsn['display_name'])
      s = ' ' + s
      s = s.split(',')
      self.street = ','.join(s[::-1])
    except:
      pass

    super(Marker, self).save(*args, **kwargs)
  
  def get_image(self):
    if self.image:
      return DOMAIN_PORT + self.image.url
    return ''