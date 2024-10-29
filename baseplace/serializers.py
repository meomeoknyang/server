from rest_framework import serializers
from .models import OperatingHours, BreakTime, BasePlace, Menu
from django.db import models
from reviews.models import Review, Keyword

class OperatingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingHours
        fields = ['day', 'start_time', 'end_time']

class BreakTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakTime
        fields = ['day', 'start_time', 'end_time']

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['name', 'price', 'image_url']

class ReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'comment', 'created_at']

class BasePlaceSerializer(serializers.ModelSerializer):
    # 메뉴 5개
    recent_menus = serializers.SerializerMethodField()
    # 키워드별 리뷰 개수
    keyword_counts = serializers.SerializerMethodField()
    # 최근 리뷰 3개
    recent_comments = serializers.SerializerMethodField()

    class Meta:
        model = BasePlace
        fields = [
            'place_id', 'name', 'opening_hours', 'image_url', 'contact',
            'address', 'phone_number', 'distance_from_gate', 'open_date',
            'average_price', 'recent_menus', 'keyword_counts', 'recent_comments'
        ]

    def get_recent_menus(self, obj):
        menus = obj.menus.all()[:5]  # 최근 5개의 메뉴만 반환
        return MenuSerializer(menus, many=True).data

    def get_keyword_counts(self, obj):
        # 키워드별 리뷰 개수
        keywords = Keyword.objects.filter(reviews__place=obj)
        keyword_counts = keywords.annotate(count=models.Count('reviews'))
        return {keyword.description: keyword.count for keyword in keyword_counts}

    def get_recent_comments(self, obj):
        # 최근 3개의 리뷰 댓글 반환
        comments = Review.objects.filter(place=obj).order_by('-created_at')[:3]
        return ReviewCommentSerializer(comments, many=True).data