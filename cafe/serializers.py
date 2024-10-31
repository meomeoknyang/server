# cafe/serializers.py
from rest_framework import serializers
from .models import Cafe, CafeCategory
from baseplace.models import Menu
from baseplace.serializers import OperatingHoursSerializer, BreakTimeSerializer
from reviews.models import Review
from django.db.models import Avg, Count

class CafeLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ['place_id','name', 'latitude', 'longitude']

class CafeCategorySerializer(serializers.ModelSerializer):
    '''
    ### 카페 카테고리 시리얼라이저
    '''
    class Meta:
        model = CafeCategory
        fields = ['id', 'name']  # 카테고리의 ID와 이름 필드만 반환

class MenuSerializer(serializers.ModelSerializer):
    '''
    ### 메뉴 시리얼라이저
    '''
    class Meta:
        model = Menu
        fields = ['id', 'name', 'price', 'description', 'image_url', 'is_special']
        ref_name = "CafeMenu"

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.nickname')  # 닉네임
    title = serializers.StringRelatedField(source='user.title')    # 칭호
    visit_count = serializers.IntegerField()                       # 몇 번째 방문인지

    class Meta:
        model = Review
        fields = ['user', 'title', 'visit_count', 'comment', 'created_at']

class CafeSerializer(serializers.ModelSerializer):
    '''
    ### 카페 시리얼라이저
    '''
    categories = CafeCategorySerializer(many=True)  # 카테고리: Many-to-Many 관계
    departments = serializers.StringRelatedField(many=True)
    # operating_hours = OperatingHoursSerializer(many=True, read_only=True)
    break_times = BreakTimeSerializer(many=True, read_only=True)
    menus = MenuSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    keywords = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Cafe
        fields = [
            'place_id', 'name', 'categories', 'opening_hours', 'image_url', 'contact',
            'distance_from_gate', 'address', 'phone_number', 'open_date', 'departments', 
            'break_times', 'menus', 'average_rating', 'keywords', 'comments'
        ]

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        cafe = Cafe.objects.create(**validated_data)

        for category_data in categories_data:
            category, created = CafeCategory.objects.get_or_create(name=category_data['name'])
            cafe.categories.add(category)

        return cafe

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', [])

        instance.name = validated_data.get('name', instance.name)
        instance.opening_hours = validated_data.get('opening_hours', instance.opening_hours)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.distance_from_gate = validated_data.get('distance_from_gate', instance.distance_from_gate)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.open_date = validated_data.get('open_date', instance.open_date)
        instance.save()

        instance.categories.clear()
        for category_data in categories_data:
            category, created = CafeCategory.objects.get_or_create(name=category_data['name'])
            instance.categories.add(category)

        return instance

    def get_menus(self, obj):
        return MenuSerializer(obj.menus.all()[:5], many=True).data

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']

    def get_keywords(self, obj):
        return (
            obj.reviews.values('keywords__description')
            .annotate(count=Count('keywords'))
            .order_by('-count')
        )

    def get_comments(self, obj):
        latest_reviews = obj.reviews.order_by('-created_at')[:3]
        return CommentSerializer(latest_reviews, many=True).data
