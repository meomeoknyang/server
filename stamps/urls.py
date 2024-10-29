# stamps/urls.py
from django.urls import path
from .views import RestaurantStampedPlaceListView, CafeStampedPlaceListView

urlpatterns = [
    # path('stamps/', StampedPlaceListView.as_view(), name='stampedplace-list'),
    path('stamps/restaurants/', RestaurantStampedPlaceListView.as_view(), name='restaurant-stamped-places'),
    path('stamps/cafe/', CafeStampedPlaceListView.as_view(), name='cafe-stamped-places'),
]

"""
식당 도장 목록 조회 (카테고리 필터링 가능):
GET /stamps/restaurants/?category_id=<카테고리 ID>

카페 도장 목록 조회 (카테고리 필터링 가능):
GET /stamps/cafes/?category_id=<카테고리 ID>
"""