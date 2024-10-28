from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, RestaurantDetailView

# DRF의 DefaultRouter 생성
router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [
    path('', include(router.urls)),  # 라우터의 URL 패턴 포함
    path('restaurants/<str:name>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
]
