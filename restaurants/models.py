from django.db import models
from baseplace.models import BasePlace, Department, BreakTime
import uuid

class Category(models.Model):
    '''
    식당 카테고리
    '''
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Restaurant(BasePlace):
    """
    categories: 여러 카테고리와 Many-to-Many 관계 설정
    """
    categories = models.ManyToManyField(Category, related_name='restaurants')
    departments = models.ManyToManyField(Department, related_name='affiliated_restaurants')  # 제휴 학과
    break_times = models.ManyToManyField(BreakTime, related_name='restaurants_break_times', blank=True)
    def __str__(self):
        return self.name
    