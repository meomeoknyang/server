# stamps/serializers.py
from rest_framework import serializers
from .models import StampedPlace
from restaurants.serializers import CategorySerializer as RestaurantCategorySerializer
from cafe.serializers import CafeCategorySerializer as CafeCategorySerializer

class StampedPlaceSerializer(serializers.ModelSerializer):
    place_id = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = StampedPlace
        fields = ['place_id', 'place', 'visit_count', 'rating', 'breaktime', 'average_price', 'distance_from_gate', 'category']
    
    def get_place_id(self, obj):
        return obj.place.place_id  # `place` 필드에서 ID를 추출하여 반환
    
    def get_category(self, obj):
        if obj.category_content_type.model == 'cafecategory':
            return CafeCategorySerializer(obj.category).data
        elif obj.category_content_type.model == 'category':  # restaurants.Category
            return RestaurantCategorySerializer(obj.category).data
        return None