# reviews/urls.py
from django.urls import path
from .views import ReviewListCreateView, UserReviewsView, PlaceReviewsView, ReviewDetailView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review-list-create'),
    path('user/<int:user_id>/', UserReviewsView.as_view(), name='user-reviews'),               # 특정 사용자의 리뷰 조회
    path('<str:place_type>/<int:place_id>/', PlaceReviewsView.as_view(), name='place-reviews'), # 특정 장소의 리뷰 조회
    path('<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),              # 특정 리뷰 상세 조회
]

"""
특정 사용자가 작성한 리뷰 조회
GET /reviews/user/<user_id>/

GET /reviews/restaurant/1/ → place_type이 restaurant이고 place_id가 1인 식당의 리뷰 조회
GET /reviews/cafe/2/ → place_type이 cafe이고 place_id가 2인 카페의 리뷰 조회

특정 리뷰 상세 조회
GET /reviews/<review_id>/
"""