import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey  # 메뉴와 리뷰를 위한 Generic Relation
from django.contrib.contenttypes.models import ContentType

class Department(models.Model): 
    '''
    제휴 학과
    '''
    name = models.CharField(max_length=100, unique=True)  # 학과 이름

    def __str__(self):
        return self.name

class BasePlace(models.Model):
    """
    Restaurant와 Cafe가 상속받을 공통 모델
    """
    place_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)  # 장소 이름
    image_url = models.URLField(max_length=500, blank=True, null=True)  # 대표 이미지 URL
    contact = models.CharField(max_length=15, blank=True, null=True)  # 연락처
    address = models.CharField(max_length=255, blank=True, null=True)  # 주소
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # 전화번호
    distance_from_gate = models.FloatField(blank=True, null=True)  # 정문에서의 거리
    open_date = models.DateField(blank=True, null=True)  # 오픈일
    departments = models.ManyToManyField(Department, related_name="places", null=True)  # 제휴 학과 다대다 관계
    average_price = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)  # 위도
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)  # 경도
    
    class Meta:
        abstract = True  # 추상 모델로 설정하여 데이터베이스에 테이블을 만들지 않음

    def __str__(self):
        return self.name

# class OperatingHours(models.Model):
#     """
#     요일별 운영 시간을 관리하는 모델
#     """
#     DAYS_OF_WEEK = [
#         ('Mon', '월요일'),
#         ('Tue', '화요일'),
#         ('Wed', '수요일'),
#         ('Thu', '목요일'),
#         ('Fri', '금요일'),
#         ('Sat', '토요일'),
#         ('Sun', '일요일'),
#     ]
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 참조할 모델의 타입
#     object_id = models.PositiveIntegerField()  # 참조할 모델의 ID
#     place = GenericForeignKey('content_type', 'object_id')  # 참조할 모델
#     # place = models.ForeignKey(BasePlace, related_name='operating_hours', on_delete=models.CASCADE)

#     day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)  # 요일
#     start_time = models.TimeField()  # 운영 시작 시간
#     end_time = models.TimeField()  # 운영 종료 시간

#     class Meta:
#         unique_together = ('content_type', 'object_id', 'day')

#     def __str__(self):
#         return f"{self.place.name} - {self.get_day_display()}: {self.start_time} ~ {self.end_time}"


class BreakTime(models.Model):
    """
    요일별 브레이크 타임을 관리하는 모델
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    place = GenericForeignKey('content_type', 'object_id')

    # day = models.CharField(max_length=3, choices=OperatingHours.DAYS_OF_WEEK)  # 요일
    start_time = models.TimeField()  # 브레이크 시작 시간
    end_time = models.TimeField()  # 브레이크 종료 시간

    class Meta:
        unique_together = ('content_type', 'object_id')

    def __str__(self):
        return f"{self.place.name} - {self.get_day_display()}: {self.start_time} ~ {self.end_time}"
    
class Menu(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    place = GenericForeignKey('content_type', 'object_id')

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    is_special = models.BooleanField(default=False)

    def __str__(self):
        place_name = getattr(self.place, 'name', None)
        if place_name:
            return f"{self.name} - {place_name}"
        return self.name