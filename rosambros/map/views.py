from django.db.models import Q
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotFound
from django.template import loader

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsOwnerProfileWithLevelModer, IsOwnerProfileWithLevelAdministrator

from .models import Marker
from .serializers import MarkerSerializer, MarkerExportSerializer

from accounts.models import UserProfile

from django.shortcuts import get_object_or_404
import base64
from io import BytesIO, StringIO
from rosambros.settings import MEDIA_ROOT, REPOSITORY_DIR, PLANTNET_API_KEY
from PIL import Image
import requests
import json
import base64
from datetime import datetime
import csv

from .utils import to_utf_8_sig

class MarkerList(APIView):
  def get(self, request, format=None):
    markers = Marker.objects.filter(status=1)
    serializer = MarkerSerializer(markers, many=True)
    return Response(serializer.data)

class MarkerDetail(APIView):
  def get(self, request, pk, format=None):
    marker = Marker.objects.get(id=pk)
    serializer = MarkerSerializer(marker)
    return Response(serializer.data)

class MarkerUpload(APIView):
  def post(self, request, format=None):
    # Проверка картинки на содержание амброзии
    img_bytes = base64.b64decode((request.data['image']))
    
    api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={PLANTNET_API_KEY}"

    data = {
      'organs': ['leaf']
    }

    files = [
       ('images', (img_bytes))
    ]

    req = requests.Request('POST', url=api_endpoint, files=files, data=data)
    prepared = req.prepare()

    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)

    result = False
    if response.status_code == 200:
      if 'Ambrosia' in json_result['bestMatch'] or 'Artemisia' in json_result['bestMatch']:
        result = True
      else:
        result = False
    else:
      result = False

    serializer = MarkerSerializer(data=request.data)
    if result == True:
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': 'Not ambrosia'}, status=status.HTTP_400_BAD_REQUEST)

class MarkerImageBase64(APIView):
  def get(self, request, pk, format=None):
    marker = get_object_or_404(Marker, id=pk)
    img_path = (str(MEDIA_ROOT) + marker.image.url.lstrip('/media/'))
    img = Image.open(img_path)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    context = {
      'image_base64': img_str,
    }

    return Response(context, status=status.HTTP_200_OK)

class MarkerDelete(APIView):
  permission_classes = [IsAuthenticated, IsOwnerProfileWithLevelModer]
  def delete(self, request, pk, format=None):
    marker = Marker.objects.get(id=pk)
    if marker.status != 1:
      return Response({"message": "This marker has been already deleted(archived)".format()}, status=status.HTTP_400_BAD_REQUEST)
    marker.status = 2 # id of archived marker
    marker.deletion_author = UserProfile.objects.get(user=request.user)
    marker.deletion_datetime = datetime.now()
    marker.save()
    return Response({"message": "Marker with id `{}` has been deleted(archived). The deletion author has been remembered".format(pk)}, status=status.HTTP_200_OK)

class MarkerExportJson(APIView):
  def get(self, request, format=None):
    markers = Marker.objects.filter(status=1)
    serializer = MarkerExportSerializer(markers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class MarkerExportCSV(APIView):
  permission_classes = [IsAuthenticated, IsOwnerProfileWithLevelModer]
  def get(self, request, format=None):
    buffer = StringIO()
    wr = csv.writer(buffer, delimiter=';', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    header = ['Координаты', 'Улица', 'Дата и время', 'Описание']
    wr.writerow(to_utf_8_sig(header))
    for marker in Marker.objects.all():
      wr.writerow(to_utf_8_sig([marker.gps, marker.street, marker.created_on.strftime("%d.%m.%Y %H:%M:%S"), marker.description]))

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=MarkersNow.csv'

    return response
  
class MarkerArchiveExportCSV(APIView):
  permission_classes = [IsAuthenticated, IsOwnerProfileWithLevelAdministrator]
  def get(self, request, format=None):
    buffer = StringIO()
    wr = csv.writer(buffer, delimiter=';', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    header = ['Координаты', 'Улица', 'Дата и время', 'Описание', 'Удаливший пользователь', 'Время удаления']
    wr.writerow(to_utf_8_sig(header))
    for marker in Marker.objects.filter(status=2):
      wr.writerow(to_utf_8_sig([marker.gps, marker.street, marker.created_on.strftime("%d.%m.%Y %H:%M:%S"), marker.description, marker.deletion_author.user.username, marker.deletion_datetime.strftime("%d.%m.%Y %H:%M:%S")]))

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ArchiveMarkersInfo.csv'

    return response