from rest_framework import serializers
from .models import Review, Keyword, ReviewImage
from users.serializers import CustomUserSerializer

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'description')

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['image']

class ReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True) #사용자 정보
    keywords = serializers.PrimaryKeyRelatedField(queryset=Keyword.objects.all(), many=True)  # 다중 키워드 필드
    images = ReviewImageSerializer(many=True, read_only=True)  # 다중 이미지 시리얼라이저 필드
    visit_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Review
        # fields = ['restaurant', 'rating', 'keywords', 'comment', 'images', 'created_at']
        fields = [
            'id', 'place', 'user', 'rating', 'comment', 'keywords', 'created_at', 'images', 'visit_count'
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  # 토큰에서 가져온 사용자 정보 할당
        keywords_data = validated_data.pop('keywords')  # 키워드 데이터 분리
        review = Review.objects.create(**validated_data)  # 리뷰 생성

        # 키워드 추가
        review.keywords.set(keywords_data)

        # 이미지 업로드가 포함된 경우 처리
        images = self.context['request'].FILES.getlist('images')
        for image in images:
            ReviewImage.objects.create(review=review, image=image)

        return review

"""
POST /api/reviews/
{
    "restaurant": 1,
    "rating": 5,
    "comment": "정말 맛있었어요!",
    "keywords": [1, 3, 5]
}
"""