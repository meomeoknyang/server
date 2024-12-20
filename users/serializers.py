from rest_framework import serializers
from .models import CustomUser
from stamps.models import StampedPlace
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from meomeoknyang.responses import CustomResponse
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist

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
        try:
            request = self.context.get('request')

            # 식당과 카페 통합 조회
            stamped_places = StampedPlace.objects.filter(
                user=obj,
                content_type__model__in=['restaurant', 'cafe']
            ).order_by('-id')[:5]  # 최신순으로 5개만 가져오기

            # 직렬화할 데이터 준비
            places = []
            from restaurants.serializers import RandomRestaurantSerializer, Restaurant
            from cafe.serializers import RandomCafeSerializer, Cafe

            for stamped_place in stamped_places:
                place = stamped_place.place  # `place`는 content_object와 동일
                if isinstance(place, Restaurant):
                    places.append({
                        "type": "restaurant",
                        "data": RandomRestaurantSerializer(place, context={'request': request}).data
                    })
                elif isinstance(place, Cafe):
                    places.append({
                        "type": "cafe",
                        "data": RandomCafeSerializer(place, context={'request': request}).data
                    })

            return places  # 통합 리스트 반환

        except Exception as e:
            print(f"[ERROR in get_recent_stamp_places]: {e}")
            return []


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