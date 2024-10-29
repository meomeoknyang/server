# baseplace/views.py
from rest_framework import generics
from .models import BasePlace
from .serializers import BasePlaceSerializer

class BasePlaceDetailView(generics.RetrieveAPIView):
    queryset = BasePlace.objects.all()
    serializer_class = BasePlaceSerializer
    lookup_field = 'place_id'  # place_id를 기반으로 조회
