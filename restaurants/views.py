from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Restaurant
from .serializers import RestaurantSerializer
from urllib.parse import unquote
from django.db.models import Count

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()  # 기본 전체 쿼리셋 설정
    serializer_class = RestaurantSerializer  # 시리얼라이저 클래스 설정

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # GET 요청에서 필터 조건 받아오기
        category_ids = request.GET.getlist('categories')  # 여러 개의 카테고리 ID
        search_name = request.GET.get('name')  # 검색할 식당 이름

        # 카테고리 필터링 (카테고리 ID가 전달된 경우)
        if category_ids:
            queryset = queryset.filter(categories__id__in=category_ids)

        # 이름 검색 필터링 (검색어가 전달된 경우)
        if search_name:
            queryset = queryset.filter(name__icontains=search_name)
        
        # 필터링된 결과를 직렬화하여 반환
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RestaurantDetailView(APIView):
    def get(self, request, place_id):
        # decoded_name = unquote(name)
        try:
            # # 이름으로 식당 검색
            # restaurant = Restaurant.objects.get(name=decoded_name)
            # serializer = RestaurantSerializer(restaurant)
            # return Response(serializer.data)
            # place_id로 식당 검색
            restaurant = Restaurant.objects.get(place_id=place_id)
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data)
        except Restaurant.DoesNotExist:
            # 식당이 존재하지 않을 때 커스텀 404 메시지를 반환
            return Response({"error": "해당하는 식당이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # 다른 예외 처리 (선택 사항)
            return Response({"error": "알 수 없는 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

