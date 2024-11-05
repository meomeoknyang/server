from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from restaurants.serializers import RestaurantSerializer
from cafe.serializers import CafeSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('user_id', 'name', 'nickname', 'email', 'password', 'password_confirm', 'department', 'title')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['username'] = validated_data['user_id']
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # 비밀번호 해싱
        user.save()
        return user

class RecentStampSerializer(serializers.Serializer):
    place_id = serializers.IntegerField()
    name = serializers.CharField()
    image_url = serializers.URLField()

class CustomUserSerializer(serializers.ModelSerializer):
    # recent_stamp_restaurants = RestaurantSerializer(many=True, read_only=True)  # 도장 리스트 시리얼라이저
    # recent_stamp_cafes = CafeSerializer(many=True, read_only=True)  # 카페 도장 리스트
    recent_stamp_places = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'user_id', 'username', 'nickname', 'name', 'email', 'department', 'title', 'recent_stamp_places')

    def get_recent_stamp_places(self, obj):
        recent_stamps = obj.get_recent_stamps()
        
        # 각각의 리스트를 개별적으로 직렬화
        restaurants = RecentStampSerializer(recent_stamps['restaurants'], many=True).data
        cafes = RecentStampSerializer(recent_stamps['cafes'], many=True).data
        
        # 두 결과를 합쳐서 반환
        return {
            "restaurants": restaurants,
            "cafes": cafes,
        }