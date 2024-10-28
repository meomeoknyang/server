from rest_framework import serializers
from .models import Review, Keyword, ReviewImage

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'description')

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['image']

class ReviewSerializer(serializers.ModelSerializer):
    images = ReviewImageSerializer(many=True, read_only=True)  # 다중 이미지 시리얼라이저 필드
    image = serializers.ImageField(required=False)  # 단일 이미지 필드
    
    class Meta:
        model = Review
        fields = ['restaurant', 'rating', 'comment', 'image', 'images', 'created_at']

"""
POST /api/reviews/
{
    "restaurant": 1,
    "rating": 5,
    "comment": "정말 맛있었어요!",
    "keywords": [1, 3, 5]
}
"""