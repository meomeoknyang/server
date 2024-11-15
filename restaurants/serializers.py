from rest_framework import serializers
from .models import Restaurant, Category
from baseplace.models import Menu
from reviews.models import Review
from django.db.models import Avg, Count
from baseplace.serializers import BreakTimeSerializer
from stamps.models import StampedPlace
from django.contrib.contenttypes.models import ContentType

class RestaurantLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['place_id','name', 'latitude', 'longitude']

class CategorySerializer(serializers.ModelSerializer):
    '''
    ### 카테고리 시리얼라이저
    '''
    class Meta:
        model = Category
        fields = ['id', 'name']  # 카테고리의 ID와 이름 필드만 반환

class MenuSerializer(serializers.ModelSerializer):
    '''
    ### 메뉴 시리얼라이저
    '''
    class Meta:
        model = Menu
        fields = ['id', 'name', 'price', 'description', 'image_url', 'is_special']  # 메뉴 관련 필드 반환
        ref_name = "RestaurantMenu"  # 추가된 ref_name

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.nickname')  # 닉네임
    title = serializers.StringRelatedField(source='user.title')  # 칭호
    visit_count = serializers.IntegerField()  # 몇 번째 방문인지

    class Meta:
        model = Review
        fields = ['user', 'title', 'visit_count', 'comment', 'created_at']

class RestaurantSerializer(serializers.ModelSerializer):
    '''
    ### 식당 시리얼라이저
    ManyToMany 관계와 ForeignKey 관계 처리
    '''
    
    categories = CategorySerializer(many=True)  # 카테고리: Many-to-Many 관계
    # menus = MenuSerializer(many=True, read_only=True)  # 메뉴: ForeignKey로 연결, ReadOnly로 처리
    menus = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    keywords = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    departments = serializers.StringRelatedField(many=True)
    break_times = BreakTimeSerializer(many=True, read_only=True)
    average_price = serializers.SerializerMethodField()
    visit_count = serializers.SerializerMethodField()  # 사용자별 방문 횟수 추가
    class Meta:
        model = Restaurant
        fields = [
            'place_id', 'name', 'categories', 'image_url', 'contact',
            'distance_from_gate', 'address', 'phone_number', 'open_date', 'departments', 
            'break_times', 'menus', 'average_rating', 'keywords', 'comments', 'average_price', 'visit_count'
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
            'average_price': {'required': False, 'allow_null': True},
        }

    # create 메서드: 카테고리를 처리하여 새 레스토랑을 생성
    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])  # 카테고리 데이터 분리
        restaurant = Restaurant.objects.create(**validated_data)  # 나머지 데이터로 레스토랑 생성

        # 카테고리 추가
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(name=category_data['name'])  # 카테고리 존재 확인 후 생성
            restaurant.categories.add(category)  # 레스토랑과 카테고리 연결

        return restaurant

    # update 메서드: 기존 레스토랑을 수정할 때 카테고리와 연결을 처리
    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', [])  # 카테고리 데이터 분리

        # 필드별 업데이트
        instance.name = validated_data.get('name', instance.name)
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
            category, created = Category.objects.get_or_create(name=category_data['name'])
            instance.categories.add(category)  # 새 카테고리 연결

        return instance
    
    def get_menus(self, obj):
        """
        Menu 데이터를 ContentType과 object_id를 통해 가져오는 메서드
        """
        try:
            content_type = ContentType.objects.get_for_model(Restaurant)
            menus = Menu.objects.filter(content_type=content_type, object_id=obj.place_id)
            return MenuSerializer(menus, many=True).data
        except ContentType.DoesNotExist:
            return []
        
    def get_average_rating(self, obj):
        # 평균 평점 계산
        average_rating = Review.objects.filter(
            content_type__model='restaurant', object_id=obj.place_id
        ).aggregate(average=Avg('rating'))['average']
        return average_rating if average_rating is not None else -1
    
    def get_keywords(self, obj):
        # Review 모델을 통해 Restaurant 관련 키워드 조회
        return (
            Review.objects.filter(content_type__model='restaurant', object_id=obj.place_id)
            .values('keywords__description')
            .annotate(count=Count('keywords'))
            .order_by('-count')
        )
    
    def get_comments(self, obj):
        # Review 모델을 통해 Restaurant 관련 리뷰 조회
        latest_reviews = Review.objects.filter(content_type__model='restaurant', object_id=obj.place_id).order_by('-created_at')[:3]
        return CommentSerializer(latest_reviews, many=True).data  # 최근 3개의 코멘트 반환
            
    # 평균 가격 가져오기 메서드
    def get_average_price(self, obj):
        return obj.average_price if obj.average_price is not None else 0  # 평균 가격이 없으면 기본값 0 반환

    def get_visit_count(self, obj):
        """
        현재 사용자와 특정 Restaurant 간의 방문 횟수 반환
        """
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                stamped_place = StampedPlace.objects.get(
                    user=user,
                    content_type=ContentType.objects.get_for_model(Restaurant),
                    object_id=obj.place_id
                )
                return stamped_place.visit_count
            except StampedPlace.DoesNotExist:
                return 0  # 방문 기록이 없는 경우
        return 0  # 인증되지 않은 사용자