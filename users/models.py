# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from restaurants.models import Restaurant

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
    recent_stamp_restaurants = models.ManyToManyField(Restaurant, blank=True, related_name='stamped_by')

    def __str__(self):
        return self.nickname

    def get_recent_stamps(self):
        return self.recent_stamp_restaurants.order_by('-id')[:10]  # 최근 방문한 최대 10개 식당 반환
