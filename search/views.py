from rest_framework.views import APIView
from rest_framework import status
from baseplace.models import Menu
from .serializers import MenuWithPlaceSerializer, SearchCafeSerializer, SearchRestaurantSerializer
from restaurants.models import Restaurant
from cafe.models import Cafe
from restaurants.serializers import RestaurantSerializer
from cafe.serializers import CafeSerializer
from meomeoknyang.responses import CustomResponse
from django.contrib.contenttypes.models import ContentType

class SearchView(APIView):
    def get(self, request, place_type):
        query = request.query_params.get("q", "").strip()  # 검색어 가져오기
        print(f"Search query: {query}")  # 검색어 확인

        if not query:
            return CustomResponse(
                status_text="error",
                message="검색어를 입력해주세요.",
                code=status.HTTP_400_BAD_REQUEST,
                data=None
            )
        
        model_map = {
            "restaurant": (Restaurant, SearchRestaurantSerializer, 7),
            "cafe": (Cafe, SearchCafeSerializer, 17)
        }

        model, serializer_class, content_type_id = model_map.get(place_type, (None, None, None))
        if model is None:
            return CustomResponse(
                status_text="error",
                message="유효하지 않은 place_type입니다. restaurant 또는 cafe 중에서 선택해주세요.",
                code=status.HTTP_400_BAD_REQUEST
            )
        
        # 메뉴 검색
        menu_results = Menu.objects.filter(
            content_type_id=content_type_id,  # 필터로 content_type_id를 사용
            name__icontains=query
        )[:10]  # 예시: 10개 제한
        print(f"Menu results: {menu_results}")  # 검색 결과 확인
        
        # 장소 검색
        place_results = model.objects.filter(name__icontains=query)[:10]
        print(f"place results: {place_results}")  # 검색 결과 확인
        
        # 시리얼라이저를 통해 JSON 데이터로 변환
        menu_data = MenuWithPlaceSerializer(menu_results, many=True).data
        place_data = serializer_class(place_results, many=True).data
        return CustomResponse(
            status_text="success",
            message=f"{place_type} 검색 결과",
            code=status.HTTP_200_OK,
            data={
                "menus": menu_data,
                "places": place_data
            }
        )
