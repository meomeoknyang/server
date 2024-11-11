# serializers.py (또는 적절한 위치에 추가)
from rest_framework import serializers
from baseplace.models import Menu
from restaurants.models import Restaurant
from cafe.models import Cafe
from restaurants.serializers import RestaurantSerializer
from cafe.serializers import CafeSerializer

class MenuWithPlaceSerializer(serializers.ModelSerializer):
    # place = serializers.SerializerMethodField()
    class Meta:
        model = Menu
        fields = ['name']

    # def get_place(self, obj):
    #     # content_type_id 값에 따라 다른 시리얼라이저로 직렬화
    #     if obj.content_type_id == 7:  # Restaurant
    #         return RestaurantSerializer(obj.place).data
    #     elif obj.content_type_id == 17:  # Cafe
    #         return CafeSerializer(obj.place).data
    #     return None

class SearchRestaurantSerializer(serializers.ModelSerializer):
    place_type = serializers.SerializerMethodField()
    class Meta:
        model = Restaurant
        fields = ['place_type', 'place_id', 'name', 'distance_from_gate', 'latitude', 'longitude']
    
    def get_place_type(self, obj):
        return "restaurant"

class SearchCafeSerializer(serializers.ModelSerializer):
    place_type = serializers.SerializerMethodField()
    class Meta:
        model = Cafe
        fields = ['place_type', 'place_id', 'name', 'distance_from_gate', 'latitude', 'longitude']
    
    def get_place_type(self, obj):
        return "cafe"