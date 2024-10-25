from django.db import models
import uuid

class Category(models.Model):
    '''
    식당 카테고리
    '''
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Department(models.Model): 
    '''
    제휴 학과
    '''
    name = models.CharField(max_length=100, unique=True)  # 학과 이름

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    '''
    store_id: 식당의 고유한 식별자로 사용 
    name: 식당 이름
    categories: 여러 카테고리와 Many-to-Many 관계 설정
    opening_hours: 식당 운영 시간
    image_url: 식당 대표 이미지 URL.
    contact: 식당 연락처
    distance_from_gate: 정문에서의 거리
    address: 식당 주소
    phone_number: 전화번호
    '''
    store_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='restaurants')
    opening_hours = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500)  # 이미지 URL 필드 추가
    contact = models.CharField(max_length=15, blank=True, null=True)  # 연락처 필드 추가
    distance_from_gate = models.FloatField()
    address = models.CharField(max_length=255)
    open_date = models.DateField(blank=True, null=True)  # 오픈일 필드
    review_count = models.IntegerField(default=0)  # 리뷰 개수 캐싱 필드
    departments = models.ManyToManyField(Department, related_name='affiliated_restaurants')  # 제휴 학과
    def __str__(self):
        return self.name

class Menu(models.Model):
    '''
    restaurant
    name
    price
    description
    image_url  메뉴 이미지
    '''
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)  # 메뉴 이미지
    is_special = models.BooleanField(default=False)  # 특별 메뉴 여부

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"