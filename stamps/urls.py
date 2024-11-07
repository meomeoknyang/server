# stamps/urls.py
from django.urls import path
from .views import  StampedPlaceTypeListView

urlpatterns = [
    path('stamps/', StampedPlaceTypeListView.as_view(), name='stampedplace-list'),
    path('stamps/<str:place_type>/', StampedPlaceTypeListView.as_view(), name='stamped-place-type-list'),
]

"""
식당 도장 목록 조회 (카테고리 필터링 가능):
GET /stamps/restaurant/?category_id=<카테고리 ID>

카페 도장 목록 조회 (카테고리 필터링 가능):
GET /stamps/cafe/?category_id=<카테고리 ID>
"""