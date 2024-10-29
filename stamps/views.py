from django.db.models import Count, Avg
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import StampedPlace
from .serializers import StampedPlaceSerializer
from django.db.models import Count, F


class RestaurantStampedPlaceListView(generics.ListAPIView):
    serializer_class = StampedPlaceSerializer

    def get_queryset(self):
        restaurant_content_type = ContentType.objects.get(app_label='restaurants', model='restaurant')

        if not self.request.user.is_authenticated:
            return StampedPlace.objects.filter(content_type=restaurant_content_type).none()

        queryset = StampedPlace.objects.filter(content_type=restaurant_content_type, user=self.request.user)

        # 카테고리 필터링
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(place__categories__id=category_id)

        # 방문 여부 필터링
        visited = self.request.query_params.get('visited')
        if visited == 'true':
            queryset = queryset.filter(visit_count__gt=0)
        elif visited == 'false':
            queryset = queryset.filter(visit_count=0)

         # 정렬 조건
        sort = self.request.query_params.get('sort')
        if sort == 'rating_desc':
            queryset = queryset.order_by(F('rating').desc(nulls_last=True))  # 평점 없는 것은 마지막으로 정렬
        elif sort == 'review_count_desc':
            queryset = queryset.annotate(review_count=Count('place__reviews')).order_by('-review_count')
        elif sort == 'open_date_asc':
            queryset = queryset.order_by(F('place__open_date').asc(nulls_last=True))
        # 준비 중
        # elif sort == 'recommended':
        #     queryset = queryset.filter(rating__gte=4).order_by(F('rating').desc(nulls_last=True))
        return queryset


    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            anonymous_data = [{
                "place_id": stamped_place.place_id,
                "place": stamped_place.place.name,
                "visit_count": -1,
                "rating": stamped_place.rating,
                "breaktime": stamped_place.breaktime,
                "average_price": stamped_place.average_price,
                "distance_from_gate": stamped_place.distance_from_gate,
            } for stamped_place in StampedPlace.objects.filter(content_type=ContentType.objects.get(app_label='restaurants', model='restaurant'))]
            return Response(anonymous_data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)


class CafeStampedPlaceListView(generics.ListAPIView):
    serializer_class = StampedPlaceSerializer

    def get_queryset(self):
        cafe_content_type = ContentType.objects.get(app_label='cafe', model='cafe')

        if not self.request.user.is_authenticated:
            return StampedPlace.objects.filter(content_type=cafe_content_type).none()

        queryset = StampedPlace.objects.filter(content_type=cafe_content_type, user=self.request.user)

        # 카테고리 필터링
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(place__categories__id=category_id)

        # 방문 여부 필터링
        visited = self.request.query_params.get('visited')
        if visited == 'true':
            queryset = queryset.filter(visit_count__gt=0)
        elif visited == 'false':
            queryset = queryset.filter(visit_count=0)

         # 정렬 조건
        sort = self.request.query_params.get('sort')
        if sort == 'rating_desc':
            queryset = queryset.order_by(F('rating').desc(nulls_last=True))  # 평점 없는 것은 마지막으로 정렬
        elif sort == 'review_count_desc':
            queryset = queryset.annotate(review_count=Count('place__reviews')).order_by('-review_count')
        elif sort == 'open_date_asc':
            queryset = queryset.order_by(F('place__open_date').asc(nulls_last=True))
        # 준비중
        # elif sort == 'recommended':
        #     queryset = queryset.filter(rating__gte=4).order_by(F('rating').desc(nulls_last=True))
        return queryset

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            anonymous_data = [{
                "place_id": stamped_place.place_id,
                "place": stamped_place.place.name,
                "visit_count": -1,
                "rating": stamped_place.rating,
                "breaktime": stamped_place.breaktime,
                "average_price": stamped_place.average_price,
                "distance_from_gate": stamped_place.distance_from_gate,
            } for stamped_place in StampedPlace.objects.filter(content_type=ContentType.objects.get(app_label='cafe', model='cafe'))]
            return Response(anonymous_data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)
