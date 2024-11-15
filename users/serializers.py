from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from meomeoknyang.responses import CustomResponse
from rest_framework.exceptions import AuthenticationFailed

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

    # def get_recent_stamp_places(self, obj):
    #     recent_stamps = obj.get_recent_stamps()
        
    #     # 각각의 리스트를 개별적으로 직렬화
    #     restaurants = RecentStampSerializer(recent_stamps['restaurants'], many=True).data
    #     cafes = RecentStampSerializer(recent_stamps['cafes'], many=True).data
        
    #     # 두 결과를 합쳐서 반환
    #     return {
    #         "restaurants": restaurants,
    #         "cafes": cafes,
    #     }
    def get_recent_stamp_places(self, obj):
    # 예외 처리로 get_recent_stamps() 호출 보장
        try:
            recent_stamps = obj.get_recent_stamps() or {}  # None일 경우 빈 dict로 초기화
        except AttributeError:
            recent_stamps = {"restaurants": [], "cafes": []}

        # restaurants와 cafes를 개별적으로 직렬화
        restaurants = recent_stamps.get('restaurants', [])
        cafes = recent_stamps.get('cafes', [])

        # 직렬화된 데이터 반환
        return {
            "restaurants": RecentStampSerializer(restaurants, many=True).data,
            "cafes": RecentStampSerializer(cafes, many=True).data,
        }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'user_id'

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # 데이터 형식을 JSON 직렬화 가능하도록 반환
        return {
            "status": "success",
            "message": "로그인 성공",
            "code": status.HTTP_200_OK,
            "data": data
        }