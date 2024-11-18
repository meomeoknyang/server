from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Restaurant
from .serializers import RestaurantSerializer, RestaurantLocationSerializer, RestaurantDetailSerializer, RandomRestaurantSerializer
from urllib.parse import unquote
from django.db.models import Count, F, Q
from rest_framework.permissions import AllowAny
from meomeoknyang.responses import CustomResponse
from baseplace.models import Menu
from django.contrib.contenttypes.models import ContentType 
from stamps.models import StampedPlace
import random

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()  # 기본 전체 쿼리셋 설정
    serializer_class = RestaurantSerializer  # 시리얼라이저 클래스 설정

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            
            # GET 요청에서 필터 조건 받아오기
            category_ids = request.GET.getlist('categories')  # categories 파라미터에서 여러 ID 가져오기

            search_name = request.GET.get('name')  # 검색할 식당 이름
            menu_name = request.GET.get('menu_name')  # 메뉴 이름 검색
            visited = request.GET.get('visited')
            
            if visited in ['true', 'false']:
                # ContentType 가져오기
                restaurant_content_type = ContentType.objects.get_for_model(Restaurant)

                # StampedPlace에서 방문 여부 필터링
                stamped_places = StampedPlace.objects.filter(
                    content_type=restaurant_content_type,
                    user=request.user
                )
                if visited == 'true':
                    stamped_places = stamped_places.filter(visit_count__gt=0)
                elif visited == 'false':
                    stamped_places = stamped_places.filter(visit_count=0)

                # 방문 기록이 있는 place_id만 필터링
                visited_place_ids = stamped_places.values_list('object_id', flat=True)
                queryset = queryset.filter(place_id__in=visited_place_ids)


            # 카테고리 필터링 (카테고리 ID가 전달된 경우)
            # if category_ids:
            #     queryset = queryset.filter(categories__id__in=category_ids)

            if category_ids:
                # 카테고리 ID의 개수
                num_categories = len(category_ids)

                # 모든 카테고리를 포함하는 식당만 조회
                queryset = queryset.filter(categories__id__in=category_ids) \
                                .annotate(num_matching_categories=Count('categories', filter=Q(categories__id__in=category_ids))) \
                                .filter(num_matching_categories=num_categories)

            # 이름 검색 필터링 (검색어가 전달된 경우)
            if search_name:
                queryset = queryset.filter(name__icontains=search_name)

            # 메뉴 이름으로 필터링
            if menu_name:
                # Menu에서 필터링 후, 해당 BasePlace를 참조하는 쿼리셋
                menu_places = Menu.objects.filter(
                    name__icontains=menu_name,
                    content_type=ContentType.objects.get_for_model(queryset.model)
                ).values_list('object_id', flat=True)
                queryset = queryset.filter(place_id__in=menu_places).distinct()

            # 필터링된 결과를 직렬화하여 반환
            serializer = self.get_serializer(queryset, many=True)
            return CustomResponse(
                status_text="success",
                message="식당 목록 조회 성공",
                code=status.HTTP_200_OK,
                data=serializer.data
            )
        except Exception as e:
            return CustomResponse(
                status_text="error",
                message="식당 목록 조회 중 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=str(e)
            )


class RestaurantDetailView(APIView):
    """
    식당 상세 정보를 조회하는 뷰
    """
    def get(self, request, place_id):
        """
        GET 요청: 특정 식당의 상세 정보 조회
        """
        print(request)  # Debug: request 객체 확인
        try:
            # 식당 객체 가져오기
            restaurant = Restaurant.objects.get(place_id=place_id)
            
            # 데이터 직렬화
            serializer = RestaurantDetailSerializer(restaurant, context={'request': request})
        
            # 성공 응답 반환
            return CustomResponse(
                status_text="success",
                message="식당 상세 정보 조회 성공",
                code=status.HTTP_200_OK,
                data=serializer.data
            )
        except Restaurant.DoesNotExist:
            # 식당이 없을 경우 404 반환
            return CustomResponse(
                status_text="error",
                message="해당하는 식당이 존재하지 않습니다.",
                code=status.HTTP_404_NOT_FOUND,
                data=None
            )
        except Exception as e:
            # 기타 예외 처리
            return CustomResponse(
                status_text="error",
                message="알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"error": str(e)}
            )


class RestaurantLocationView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantLocationSerializer
    lookup_field = 'place_id'

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return CustomResponse(
                status_text="success",
                message="식당 위치 정보 조회 성공",
                code=status.HTTP_200_OK,
                data=response.data
            )
        except Restaurant.DoesNotExist:
            return CustomResponse(
                status_text="error",
                message="해당 식당의 위치 정보를 찾을 수 없습니다.",
                code=status.HTTP_404_NOT_FOUND,
                data=str(e)
            )
        except Exception as e:
            return CustomResponse(
                status_text="error",
                message="알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=str(e)
            )

class FilteredRestaurantLocationView(generics.ListAPIView):
    serializer_class = RestaurantLocationSerializer
    permission_classes = [AllowAny]  # 비회원 접근 허용

    def get_queryset(self):
        queryset = Restaurant.objects.all()

        # 방문 여부 필터링
        visited = self.request.GET.get('visited')
                # 익명 사용자 처리
        user = self.request.user
        if not user.is_authenticated:
            # 익명 사용자의 경우 빈 QuerySet 반환
            return queryset.none()
        
        if visited in ['true', 'false']:
            # ContentType 가져오기
            restaurant_content_type = ContentType.objects.get_for_model(Restaurant)

            # StampedPlace에서 방문 여부 필터링
            stamped_places = StampedPlace.objects.filter(
                content_type=restaurant_content_type,
                user=self.request.user
            )
            if visited == 'true':
                stamped_places = stamped_places.filter(visit_count__gt=0)
            elif visited == 'false':
                stamped_places = stamped_places.filter(visit_count=0)

                # 방문 기록이 있는 place_id만 필터링
            visited_place_ids = stamped_places.values_list('object_id', flat=True)
            queryset = queryset.filter(place_id__in=visited_place_ids)

        # 카테고리 필터링
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        # 정렬 조건
        sort = self.request.query_params.get('sort')
        if sort == 'rating_desc':
            queryset = queryset.order_by(F('rating').desc(nulls_last=True))
        elif sort == 'review_count_desc':
            queryset = queryset.annotate(review_count=Count('reviews')).order_by('-review_count')
        elif sort == 'open_date_asc':
            queryset = queryset.order_by(F('open_date').asc(nulls_last=True))

        return queryset.filter(latitude__isnull=False, longitude__isnull=False)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            data = self.get_serializer(queryset, many=True).data
            return CustomResponse(
                status_text="success",
                message="필터링된 식당 위치 목록 조회 성공",
                code=status.HTTP_200_OK,
                data=data
            )
        except Exception as e:
            return CustomResponse(
                status_text="error",
                message="식당 위치 목록을 불러오는 중 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None
            )
        
class RandomRestaurantView(APIView):
    def get(self, request):
        try:
            restaurant_count = Restaurant.objects.count()  # 총 식당 개수 가져오기
            if restaurant_count == 0:
                return CustomResponse(
                    status_text="error",
                    message="등록된 식당이 없습니다.",
                    code=status.HTTP_404_NOT_FOUND,
                    data=None
                )
            random_index = random.randint(0, restaurant_count - 1)  # 랜덤 인덱스 생성
            random_restaurant = Restaurant.objects.all()[random_index]  # 랜덤 식당 가져오기
            serializer = RandomRestaurantSerializer(random_restaurant, context={'request': request})
            return CustomResponse(
                status_text="success",
                message="랜덤 식당 정보 조회 성공",
                code=status.HTTP_200_OK,
                data=serializer.data
            )
        except Exception as e:
            return CustomResponse(
                status_text="error",
                message="알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"error": str(e)}
            )
        
class RestaurantLocationDetailView(APIView):
    """
    식당 상세 정보를 조회하는 뷰
    """
    def get(self, request, place_id):
        """
        GET 요청: 특정 식당의 상세 정보 조회
        """
        print(request)  # Debug: request 객체 확인
        try:
            # 식당 객체 가져오기
            restaurant = Restaurant.objects.get(place_id=place_id)
            
            # 데이터 직렬화
            serializer = RestaurantDetailSerializer(restaurant, context={'request': request})
        
            # 성공 응답 반환
            return CustomResponse(
                status_text="success",
                message="식당 상세 정보 조회 성공",
                code=status.HTTP_200_OK,
                data=serializer.data
            )
        except Restaurant.DoesNotExist:
            # 식당이 없을 경우 404 반환
            return CustomResponse(
                status_text="error",
                message="해당하는 식당이 존재하지 않습니다.",
                code=status.HTTP_404_NOT_FOUND,
                data=None
            )
        except Exception as e:
            # 기타 예외 처리
            return CustomResponse(
                status_text="error",
                message="알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"error": str(e)}
            )