# cafe/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CafeViewSet, CafeDetailView

# DRF의 DefaultRouter 생성
router = DefaultRouter()
router.register(r'cafes', CafeViewSet)

urlpatterns = [
    path('', include(router.urls)),  # 라우터의 URL 패턴 포함
    # place_id로 단일 조회
    path('cafes/<uuid:place_id>/', CafeDetailView.as_view(), name='cafe-detail'),
]
