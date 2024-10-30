# cafe/urls.py
from django.urls import path, include
from .views import CafeViewSet, CafeDetailView, CafeLocationView, FilteredCafeLocationView

urlpatterns = [
    path('cafes/', CafeViewSet.as_view({'get': 'list', 'post': 'create'}), name='cafe-list'),
    # place_id로 단일 조회
    path('cafes/<int:place_id>/', CafeDetailView.as_view(), name='cafe-detail'),
    path('cafes/<int:place_id>/location/', CafeLocationView.as_view(), name='cafe-location'),
    path('cafes/locations/', FilteredCafeLocationView.as_view(), name='filtered-cafe-locations'),
]
