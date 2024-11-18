from rest_framework import serializers
from .models import Review, Keyword, ReviewImage
from users.serializers import CustomUserSerializer
from django.contrib.contenttypes.models import ContentType
from meomeoknyang import settings
class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'description')

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['image']

class ReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # 사용자 정보
    keywords = serializers.PrimaryKeyRelatedField(queryset=Keyword.objects.all(), many=True)  # 다중 키워드 필드
    images = ReviewImageSerializer(many=True, read_only=True)  # 다중 이미지 시리얼라이저 필드
    visit_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'rating', 'comment', 'keywords', 'created_at', 'images', 'visit_count'
        ]

    def create(self, validated_data):
        user = self.context['request'].user  # 현재 사용자
        place_type = self.context['place_type']
        place_id = self.context['place_id']

        # ContentType 설정
        if place_type == 'restaurant':
            content_type = ContentType.objects.get(app_label='restaurants', model='restaurant')
        elif place_type == 'cafe':
            content_type = ContentType.objects.get(app_label='cafe', model='cafe')
        else:
            raise serializers.ValidationError("Invalid 'place_type' value. Must be 'restaurant' or 'cafe'.")

        keywords_data = validated_data.pop('keywords', [])

        # Review 생성
        review = Review.objects.create(
            user=user,
            content_type=content_type,
            object_id=place_id,
            **validated_data
        )
        review.keywords.set(keywords_data)

        # 이미지 처리
        images = self.context['request'].FILES.getlist('images', [])
        for image in images:
            review_image = ReviewImage.objects.create(review=review, image=image)
            print(f"Saved {review_image.image.name} to {settings.DEFAULT_FILE_STORAGE}")

        return review
