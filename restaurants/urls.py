from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, RestaurantDetailView, RestaurantLocationView, FilteredRestaurantLocationView

urlpatterns = [
    path('restaurants/', RestaurantViewSet.as_view({'get': 'list', 'post': 'create'}), name='restaurant-list'),
    path('restaurants/<int:place_id>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurants/<int:place_id>/location/', RestaurantLocationView.as_view(), name='restaurant-location'),  # 단일 위치 조회
    path('restaurants/locations/', FilteredRestaurantLocationView.as_view(), name='filtered-restaurant-locations'),  # 여러 위치 필터링 조회
]
