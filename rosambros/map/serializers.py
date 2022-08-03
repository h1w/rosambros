from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Marker
import re
from PIL import Image

class MarkerExportSerializer(serializers.ModelSerializer):
  class Meta:
    model = Marker
    fields = (
      'street',
      'gps',
      'created_on',
      'description',
    )

class MarkerSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    class Meta:
        model = Marker
        fields = (
            'id',
            'street',
            'name',
            'description',
            'gps',
            'image',
            'get_image',
            'created_on',
        )
    
    def validate(self, data):
        gps = data['gps']

        pattern = '^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'
        match_result = re.match(pattern, gps)

        if match_result:
            pass
        else:
            error = { 'message': 'Validation error. Your data: {} is invalid.'.format(gps) }
            raise serializers.ValidationError(error)
        
        return data