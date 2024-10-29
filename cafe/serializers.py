# cafe/serializers.py
from rest_framework import serializers
from .models import Cafe, CafeCategory
from baseplace.serializers import OperatingHoursSerializer, BreakTimeSerializer

class CafeCategorySerializer(serializers.ModelSerializer):
    '''
    ### 카페 카테고리 시리얼라이저
    '''
    class Meta:
        model = CafeCategory
        fields = ['id', 'name']  # 카테고리의 ID와 이름 필드만 반환

class CafeSerializer(serializers.ModelSerializer):
    '''
    ### 카페 시리얼라이저
    ManyToMany 관계와 ForeignKey 관계 처리
    '''
    
    categories = CafeCategorySerializer(many=True)  # 카테고리: Many-to-Many 관계
    departments = serializers.StringRelatedField(many=True)
    operating_hours = OperatingHoursSerializer(many=True, read_only=True)
    break_times = BreakTimeSerializer(many=True, read_only=True)

    class Meta:
        model = Cafe
        fields = [
            'place_id', 'name', 'categories', 'opening_hours', 'image_url', 'contact',
            'distance_from_gate', 'address', 'phone_number', 'open_date', 'departments', 
            'operating_hours', 'break_times'
        ]

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])  # 카테고리 데이터 분리
        cafe = Cafe.objects.create(**validated_data)  # 나머지 데이터로 카페 생성

        # 카테고리 추가
        for category_data in categories_data:
            category, created = CafeCategory.objects.get_or_create(name=category_data['name'])  # 카테고리 존재 확인 후 생성
            cafe.categories.add(category)  # 카페와 카테고리 연결

        return cafe

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', [])  # 카테고리 데이터 분리

        # 필드별 업데이트
        instance.name = validated_data.get('name', instance.name)
        instance.opening_hours = validated_data.get('opening_hours', instance.opening_hours)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.distance_from_gate = validated_data.get('distance_from_gate', instance.distance_from_gate)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.open_date = validated_data.get('open_date', instance.open_date)
        instance.save()

        # 카테고리 업데이트
        instance.categories.clear()  # 기존 카테고리 연결 제거
        for category_data in categories_data:
            category, created = CafeCategory.objects.get_or_create(name=category_data['name'])
            instance.categories.add(category)  # 새 카테고리 연결

        return instance
