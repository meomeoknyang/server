# cafe/models.py
import uuid
from django.db import models
from baseplace.models import BasePlace, Department, BreakTime
from restaurants.models import Category

class CafeCategory(models.Model):
    '''
    카페 카테고리
    '''
    id = models.BigAutoField(primary_key=True)
    CATEGORY_CHOICES = [
        ('카공', '카공'),
        ('디저트', '디저트'),
        ('빵', '빵'),
        ('테이크아웃', '테이크아웃'),
    ]

    name = models.CharField(max_length=50, choices= CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Cafe(BasePlace):
    """
    Cafe 모델 - BasePlace를 상속받아 카페의 기본 정보를 저장
    """
    categories = models.ManyToManyField(CafeCategory, related_name='cafes')  # 카페 카테고리
    departments = models.ManyToManyField(Department, related_name='affiliated_cafes')  # 제휴 학과
    break_times = models.ManyToManyField(BreakTime, related_name='cafe_break_times', blank=True)

    def __str__(self):
        return self.name
