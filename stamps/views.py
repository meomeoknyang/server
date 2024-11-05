from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, status
from rest_framework.response import Response
from .models import StampedPlace
from .serializers import StampedPlaceSerializer
from django.db.models import Count, F
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from meomeoknyang.responses import CustomResponse

# 공통 필터 및 정렬 기능 함수
def apply_filters_and_sorting(queryset, request):
    # 카테고리 필터링
    category_id = request.query_params.get('category_id')
    if category_id:
        queryset = queryset.filter(place__categories__id=category_id)

    # 방문 여부 필터링
    visited = request.query_params.get('visited')
    if visited == 'true':
        queryset = queryset.filter(visit_count__gt=0)
    elif visited == 'false':
        queryset = queryset.filter(visit_count=0)

    # 정렬 조건
    sort = request.query_params.get('sort')
    if sort == 'rating_desc':
        queryset = queryset.order_by(F('rating').desc(nulls_last=True))
    elif sort == 'review_count_desc':
        queryset = queryset.annotate(review_count=Count('place__reviews')).order_by('-review_count')
    elif sort == 'open_date_asc':
        queryset = queryset.order_by(F('place__open_date').asc(nulls_last=True))
    return queryset

# 모든 장소의 도장 데이터
class StampedPlaceListView(generics.ListAPIView):
    serializer_class = StampedPlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return StampedPlace.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                anonymous_data = [{
                    "place_id": stamped_place.place.place_id,
                    "place": stamped_place.place.name,
                    "visit_count": -1,
                    "rating": stamped_place.rating,
                    "breaktime": stamped_place.breaktime,
                    "average_price": stamped_place.average_price,
                    "distance_from_gate": stamped_place.distance_from_gate,
                } for stamped_place in self.get_queryset()]

                return CustomResponse(
                    status_text="success",
                    message="비회원 사용자에게 기본 데이터 반환",
                    code=status.HTTP_200_OK,
                    data=anonymous_data
                )

            queryset = apply_filters_and_sorting(self.get_queryset(), request)
            serializer = self.get_serializer(queryset, many=True)
            return CustomResponse(
                status_text="success",
                message="회원 사용자에게 전체 데이터 반환",
                code=status.HTTP_200_OK,
                data=serializer.data
            )
        except Exception as e:
                return CustomResponse(
                    status_text="error",
                    message="도장 데이터를 가져오는 중 오류가 발생했습니다.",
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data=None
                )

# class RestaurantStampedPlaceListView(generics.ListAPIView):
#     serializer_class = StampedPlaceSerializer

#     def get_queryset(self):
#         restaurant_content_type = ContentType.objects.get(app_label='restaurants', model='restaurant')

#         if not self.request.user.is_authenticated:
#             return StampedPlace.objects.filter(content_type=restaurant_content_type).none()

#         queryset = StampedPlace.objects.filter(content_type=restaurant_content_type, user=self.request.user)

#         # 카테고리 필터링
#         category_id = self.request.query_params.get('category_id')
#         if category_id:
#             queryset = queryset.filter(place__categories__id=category_id)

#         # 방문 여부 필터링
#         visited = self.request.query_params.get('visited')
#         if visited == 'true':
#             queryset = queryset.filter(visit_count__gt=0)
#         elif visited == 'false':
#             queryset = queryset.filter(visit_count=0)

#          # 정렬 조건
#         sort = self.request.query_params.get('sort')
#         if sort == 'rating_desc':
#             queryset = queryset.order_by(F('rating').desc(nulls_last=True))  # 평점 없는 것은 마지막으로 정렬
#         elif sort == 'review_count_desc':
#             queryset = queryset.annotate(review_count=Count('place__reviews')).order_by('-review_count')
#         elif sort == 'open_date_asc':
#             queryset = queryset.order_by(F('place__open_date').asc(nulls_last=True))
#         # 준비 중
#         # elif sort == 'recommended':
#         #     queryset = queryset.filter(rating__gte=4).order_by(F('rating').desc(nulls_last=True))
#         return queryset


#     def list(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             anonymous_data = [{
#                 "place_id": stamped_place.place_id,
#                 "place": stamped_place.place.name,
#                 "visit_count": -1,
#                 "rating": stamped_place.rating,
#                 "breaktime": stamped_place.breaktime,
#                 "average_price": stamped_place.average_price,
#                 "distance_from_gate": stamped_place.distance_from_gate,
#             } for stamped_place in StampedPlace.objects.filter(content_type=ContentType.objects.get(app_label='restaurants', model='restaurant'))]
#             return Response(anonymous_data, status=status.HTTP_200_OK)
#         return super().list(request, *args, **kwargs)


# class CafeStampedPlaceListView(generics.ListAPIView):
#     serializer_class = StampedPlaceSerializer

#     def get_queryset(self):
#         cafe_content_type = ContentType.objects.get(app_label='cafe', model='cafe')

#         if not self.request.user.is_authenticated:
#             return StampedPlace.objects.filter(content_type=cafe_content_type).none()

#         queryset = StampedPlace.objects.filter(content_type=cafe_content_type, user=self.request.user)

#         # 카테고리 필터링
#         category_id = self.request.query_params.get('category_id')
#         if category_id:
#             queryset = queryset.filter(place__categories__id=category_id)

#         # 방문 여부 필터링
#         visited = self.request.query_params.get('visited')
#         if visited == 'true':
#             queryset = queryset.filter(visit_count__gt=0)
#         elif visited == 'false':
#             queryset = queryset.filter(visit_count=0)

#          # 정렬 조건
#         sort = self.request.query_params.get('sort')
#         if sort == 'rating_desc':
#             queryset = queryset.order_by(F('rating').desc(nulls_last=True))  # 평점 없는 것은 마지막으로 정렬
#         elif sort == 'review_count_desc':
#             queryset = queryset.annotate(review_count=Count('place__reviews')).order_by('-review_count')
#         elif sort == 'open_date_asc':
#             queryset = queryset.order_by(F('place__open_date').asc(nulls_last=True))
#         # 준비중
#         # elif sort == 'recommended':
#         #     queryset = queryset.filter(rating__gte=4).order_by(F('rating').desc(nulls_last=True))
#         return queryset

#     def list(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             anonymous_data = [{
#                 "place_id": stamped_place.place_id,
#                 "place": stamped_place.place.name,
#                 "visit_count": -1,
#                 "rating": stamped_place.rating,
#                 "breaktime": stamped_place.breaktime,
#                 "average_price": stamped_place.average_price,
#                 "distance_from_gate": stamped_place.distance_from_gate,
#             } for stamped_place in StampedPlace.objects.filter(content_type=ContentType.objects.get(app_label='cafe', model='cafe'))]
#             return Response(anonymous_data, status=status.HTTP_200_OK)
#         return super().list(request, *args, **kwargs)

class StampedPlaceTypeListView(generics.ListAPIView):
    serializer_class = StampedPlaceSerializer

    def get_queryset(self, place_type):
        try:
            if place_type == 'restaurant':
                content_type = ContentType.objects.get(app_label='restaurants', model='restaurant')
            elif place_type == 'cafe':
                content_type = ContentType.objects.get(app_label='cafe', model='cafe')
            else:
                return None  # 유효하지 않은 place_type인 경우 None 반환
        except ContentType.DoesNotExist:
            return None  # ContentType이 존재하지 않으면 None 반환
        
        if not self.request.user.is_authenticated:
            return StampedPlace.objects.filter(content_type=content_type).none()
        
        return StampedPlace.objects.filter(content_type=content_type, user=self.request.user)

    def list(self, request, *args, **kwargs):
        place_type = kwargs.get("place_type")
        queryset = self.get_queryset(place_type)
        
        if queryset is None:
            # 유효하지 않은 place_type이거나 ContentType이 없는 경우
            return CustomResponse(
                status_text="error",
                message="유효하지 않은 장소 타입입니다.",
                code=status.HTTP_400_BAD_REQUEST,
                data=None
            )

        if not request.user.is_authenticated:
            anonymous_data = [{
                "place_id": stamped_place.place_id,
                "place": stamped_place.place.name,
                "visit_count": -1,
                "rating": stamped_place.rating,
                "breaktime": stamped_place.breaktime,
                "average_price": stamped_place.average_price,
                "distance_from_gate": stamped_place.distance_from_gate,
            } for stamped_place in queryset]
            return CustomResponse(
                status_text="success",
                message=f"{place_type.capitalize()} 데이터 반환",
                code=status.HTTP_200_OK,
                data=anonymous_data
            )

        queryset = apply_filters_and_sorting(queryset, request)
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(
            status_text="success",
            message=f"{place_type.capitalize()} 스탬프 데이터 반환",
            code=status.HTTP_200_OK,
            data=serializer.data
        )
