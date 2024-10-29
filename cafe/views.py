# cafe/views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cafe
from .serializers import CafeSerializer, CafeLocationSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics

class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all()  # 기본 전체 쿼리셋 설정
    serializer_class = CafeSerializer  # 시리얼라이저 클래스 설정

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # GET 요청에서 필터 조건 받아오기
        category_ids = request.GET.getlist('categories')  # 여러 개의 카테고리 ID
        search_name = request.GET.get('name')  # 검색할 카페 이름

        # 카테고리 필터링 (카테고리 ID가 전달된 경우)
        if category_ids:
            queryset = queryset.filter(categories__id__in=category_ids)

        # 이름 검색 필터링 (검색어가 전달된 경우)
        if search_name:
            queryset = queryset.filter(name__icontains=search_name)
        
        # 필터링된 결과를 직렬화하여 반환
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CafeDetailView(APIView):
    def get(self, request, place_id):
        # place_id로 카페 검색
        cafe = get_object_or_404(Cafe, place_id=place_id)
        serializer = CafeSerializer(cafe)
        return Response(serializer.data)

class CafeLocationView(generics.RetrieveAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeLocationSerializer
    lookup_field = 'place_id'