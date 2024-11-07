from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, status
from rest_framework.response import Response
from .models import StampedPlace
from .serializers import StampedPlaceSerializer
from django.db.models import Count, F
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from meomeoknyang.responses import CustomResponse
from cafe.models import Cafe
from restaurants.models import Restaurant

def apply_filters_and_sorting(queryset, request, place_type):
    # 카테고리 필터링
    category_id = request.query_params.get('category_id')
    if category_id:
        category_id = int(category_id)
        queryset = [
            stamped_place for stamped_place in queryset
            if any(cat.id == category_id for cat in stamped_place.place.categories.all())
        ]

    # 방문 여부 필터링
    visited = request.query_params.get('visited')
    if visited == 'true':
        queryset = [stamped_place for stamped_place in queryset if stamped_place.visit_count > 0]
    elif visited == 'false':
        queryset = [stamped_place for stamped_place in queryset if stamped_place.visit_count == 0]

    # 정렬 조건
    sort = request.query_params.get('sort')
    if sort == 'rating_desc':
        queryset.sort(key=lambda x: (x.rating is None, x.rating), reverse=True)
    elif sort == 'review_count_desc':
        queryset.sort(key=lambda x: x.place.review_count, reverse=True)
    elif sort == 'open_date_asc':
        queryset.sort(key=lambda x: x.place.open_date if x.place.open_date else float('inf'))
    return queryset

# 장소 유형 및 ContentType 설정 함수
def get_content_type_and_places(place_type):
    if place_type == 'restaurant':
        return ContentType.objects.get_for_model(Restaurant), Restaurant.objects.all()
    elif place_type == 'cafe':
        return ContentType.objects.get_for_model(Cafe), Cafe.objects.all()
    return None, None

# StampedPlace 뷰셋 통합 (비회원 및 회원 처리)
class StampedPlaceTypeListView(generics.ListAPIView):
    serializer_class = StampedPlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, content_type, user=None):
        # 비회원: 모든 장소에 대해 기본값 반환
        if user is None:
            return [
                StampedPlace(
                    content_type=content_type,
                    object_id=place.place_id,
                    visit_count=-1,
                    rating=None,
                    breaktime=None,
                    average_price=None,
                    distance_from_gate=place.distance_from_gate,
                    place=place
                ) for place in self.all_places
            ]

        # 회원: 사용자별 `StampedPlace` 데이터 반환
        user_stamped_places = StampedPlace.objects.filter(content_type=content_type, user=user).select_related('place')
        user_stamped_places_dict = {stamp.object_id: stamp for stamp in user_stamped_places}

        return [
            user_stamped_places_dict.get(
                place.place_id,
                StampedPlace(
                    content_type=content_type,
                    object_id=place.place_id,
                    visit_count=0,  # 기본값
                    rating=None,
                    breaktime=None,
                    average_price=None,
                    distance_from_gate=place.distance_from_gate,
                    place=place
                )
            ) for place in self.all_places
        ]

    def list(self, request, *args, **kwargs):
        place_type = kwargs.get("place_type")
        content_type, self.all_places = get_content_type_and_places(place_type)

        if content_type is None:
            return CustomResponse(
                status_text="error",
                message="유효하지 않은 장소 타입입니다.",
                code=status.HTTP_400_BAD_REQUEST,
                data=None
            )

        user = request.user if request.user.is_authenticated else None
        queryset = self.get_queryset(content_type, user)

        # 비회원용 기본 데이터 직렬화
        if not user:
            anonymous_data = [{
                "place_id": stamped_place.object_id,
                "place": stamped_place.place.name,
                "visit_count": stamped_place.visit_count,
                "rating": stamped_place.rating,
                "breaktime": stamped_place.breaktime,
                "average_price": stamped_place.average_price,
                "distance_from_gate": stamped_place.distance_from_gate,
                "category": [cat.name for cat in stamped_place.place.categories.all()] if hasattr(stamped_place.place, 'categories') else []
            } for stamped_place in queryset]
            return CustomResponse(
                status_text="success",
                message=f"{place_type.capitalize()} 데이터 반환",
                code=status.HTTP_200_OK,
                data=anonymous_data
            )

        # 회원 사용자용 데이터 처리 (필터 및 정렬 적용 후 반환)
        queryset = apply_filters_and_sorting(queryset, request, place_type)
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(
            status_text="success",
            message=f"{place_type.capitalize()} 스탬프 데이터 반환",
            code=status.HTTP_200_OK,
            data=serializer.data
        )