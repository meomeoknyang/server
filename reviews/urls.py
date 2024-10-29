# reviews/urls.py
from django.urls import path
from .views import ReviewListCreateView, UserReviewsView, RestaurantReviewsView, ReviewDetailView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review-list-create'),
    path('user/<int:user_id>/', UserReviewsView.as_view(), name='user-reviews'),               # 특정 사용자의 리뷰 조회
    path('restaurant/<int:restaurant_id>/', RestaurantReviewsView.as_view(), name='restaurant-reviews'),  # 특정 식당의 리뷰 조회
    path('<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),                # 특정 리뷰 상세 조회
]

"""
특정 사용자가 작성한 리뷰 조회
GET /reviews/user/<user_id>/

특정 식당의 리뷰 전체 조회
GET /reviews/restaurant/<restaurant_id>/

특정 리뷰 상세 조회
GET /reviews/<review_id>/
"""