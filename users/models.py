# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
# from restaurants.models import Restaurant
# from cafe.models import Cafe
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from baseplace.models import BasePlace


class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, email, password=None, **extra_fields):
        if not user_id:
            raise ValueError("The User ID field must be set")
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(user_id=user_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_id, email, password, **extra_fields)

class CustomUser(AbstractUser):
    TITLE_CHOICES = [
        ('haksa', '깨작 학사'),
        ('seoksa', '냠냠 석사'),
        ('baksa', '쩝쩝 박사'),
        ('kyosu', '꿀꺽 교수'),
    ]
    user_id = models.CharField(max_length=20, unique=True)  # 새로운 아이디 필드 추가
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default='haksa')
    nickname = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    # recent_stamp_restaurants = models.ManyToManyField(Restaurant, blank=True, related_name='stamped_by')
    # recent_stamp_cafes = models.ManyToManyField(Cafe, blank=True, related_name='stamped_by')

    # Generic relation
    recent_stamp_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    recent_stamp_object_id = models.PositiveIntegerField(null=True)
    recent_stamp_places = GenericForeignKey('recent_stamp_content_type', 'recent_stamp_object_id')

    USERNAME_FIELD = 'user_id'  # Django 인증에 user_id를 사용
    REQUIRED_FIELDS = ['email', 'username']  # 다른 필드를 필수로 설정하지 않음

    objects = CustomUserManager()  # CustomUserManager로 설정

    def __str__(self):
        return self.nickname

    # def get_recent_stamps(self):
    #     return self.recent_stamp_restaurants.order_by('-id')[:10]  # 최근 방문한 최대 10개 식당 반환

    def get_recent_stamps(self):
        # recent_stamp_places가 None일 경우 빈 리스트 반환
        if not self.recent_stamp_places:
            return []
        return self.recent_stamp_places.all().order_by('-id')[:10]