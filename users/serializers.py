from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from restaurants.serializers import RestaurantSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('user_id', 'nickname', 'email', 'password', 'password_confirm', 'department', 'title')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    recent_stamp_restaurants = RestaurantSerializer(many=True, read_only=True)  # 도장 리스트 시리얼라이저

    class Meta:
        model = CustomUser
        fields = ('id', 'user_id', 'username', 'nickname', 'name', 'email', 'department', 'title', 'recent_stamp_restaurants')