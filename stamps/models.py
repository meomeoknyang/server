from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class StampedPlace(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stamped_places")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('restaurant', 'cafe')})
    object_id = models.PositiveIntegerField()
    place = GenericForeignKey('content_type', 'object_id')
    
    # 카테고리를 위한 GenericForeignKey 추가
    category_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, related_name='stamped_place_categories')
    category_object_id = models.PositiveIntegerField(null=True)
    category = GenericForeignKey('category_content_type', 'category_object_id')

    visit_count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(null=True, blank=True)  # 별점 평균 (리뷰에서 계산해서 저장)
    breaktime = models.CharField(max_length=100, blank=True, null=True)  # 장소의 브레이크 타임 정보
    average_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # 장소의 평균 가격 (나중에 BasePlace에 추가 예정)
    distance_from_gate = models.FloatField(blank=True, null=True)  # 정문에서의 거리

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} - {self.place} - {self.visit_count}회 방문"
