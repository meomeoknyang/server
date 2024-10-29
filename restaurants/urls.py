from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, RestaurantDetailView, RestaurantLocationView

# DRF의 DefaultRouter 생성
router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [
    path('', include(router.urls)),  # 라우터의 URL 패턴 포함

    # place_id로 단일 조회
    path('restaurants/<uuid:place_id>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    #GET /restaurants/<place_id>/ 

    path('restaurants/<uuid:place_id>/location/', RestaurantLocationView.as_view(), name='restaurant-location'),
]
