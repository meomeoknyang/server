# cafe/serializers.py
from rest_framework import serializers
from .models import Cafe, CafeCategory
from baseplace.models import Menu
from baseplace.serializers import BreakTimeSerializer
from reviews.models import Review
from django.db.models import Avg, Count
from django.contrib.contenttypes.models import ContentType

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
    average_price = serializers.SerializerMethodField()

    class Meta:
        model = Cafe
        fields = [
            'place_id', 'name', 'categories', 'image_url', 'contact',
            'distance_from_gate', 'address', 'phone_number', 'open_date', 'departments', 
            'break_times', 'menus', 'average_rating', 'keywords', 'comments', 'averate_price'
        ]
        extra_kwargs = {
            'image_url': {'required': False, 'allow_null': True},
            'contact': {'required': False, 'allow_null': True},
            'distance_from_gate': {'required': False, 'allow_null': True},
            'address': {'required': False, 'allow_null': True},
            'phone_number': {'required': False, 'allow_null': True},
            'departments': {'required': False, 'allow_null': True},
            'break_times': {'required': False, 'allow_null': True},
            'menus': {'required': False, 'allow_null': True},
            'average_rating': {'required': False, 'allow_null': True},
            'keywords': {'required': False, 'allow_null': True},
            'comments': {'required': False, 'allow_null': True},
            'averate_price': {'required': False, 'allow_null': True},
        }

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
        # 평균 평점 계산
        average_rating = Review.objects.filter(
            content_type__model='cafe', object_id=obj.place_id
        ).aggregate(average=Avg('rating'))['average']
        return average_rating if average_rating is not None else -1
    
    def get_keywords(self, obj):
        # Review 모델을 통해 Restaurant 관련 키워드 조회
        return (
            Review.objects.filter(content_type__model='cafe', object_id=obj.place_id)
            .values('keywords__description')
            .annotate(count=Count('keywords'))
            .order_by('-count')
        )
    
    def get_comments(self, obj):
        # Review 모델을 통해 Restaurant 관련 리뷰 조회
        latest_reviews = Review.objects.filter(content_type__model='cafe', object_id=obj.place_id).order_by('-created_at')[:3]
        return CommentSerializer(latest_reviews, many=True).data  # 최근 3개의 코멘트 반환