# reviews/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Review
from .serializers import ReviewSerializer
from users.models import CustomUser

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# 특정 사용자가 작성한 리뷰 전체 조회
class UserReviewsView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        reviews = Review.objects.filter(user=user)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 특정 장소(Restaurant or Cafe)의 리뷰 전체 조회
class PlaceReviewsView(APIView):
    def get(self, request, place_type, place_id):
        # ContentType을 이용하여 place_type을 모델로 변환
        if place_type == 'restaurant':
            content_type = ContentType.objects.get(app_label='restaurants', model='restaurant')
        elif place_type == 'cafe':
            content_type = ContentType.objects.get(app_label='cafe', model='cafe')
        else:
            return Response({"error": "Invalid place type"}, status=status.HTTP_400_BAD_REQUEST)

        # 특정 장소에 대한 리뷰 필터링
        reviews = Review.objects.filter(content_type=content_type, object_id=place_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 특정 리뷰 상세 조회
class ReviewDetailView(APIView):
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)