from django.db import models
from restaurants.models import Restaurant
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Max

class Keyword(models.Model):
    description = models.CharField(max_length=100, unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True)
    place = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.description


class Review(models.Model):
    # restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)  # 작성자 필드
    rating = models.PositiveSmallIntegerField()  # 별점 (1~5)
    comment = models.TextField(blank=True, null=True)  # 리뷰 코멘트
    keywords = models.ManyToManyField(Keyword, related_name='reviews')  # 중복 선택 가능한 키워드
    created_at = models.DateTimeField(auto_now_add=True)  # 리뷰 작성 날짜
    visit_count = models.PositiveIntegerField(default=1) # 방문 횟수
    # GenericForeignKey를 사용하여 BasePlace 상속 모델과의 관계 정의
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    place = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        # 사용자가 특정 장소에 남긴 리뷰 중 가장 높은 visit_count 값을 가져옴
        last_visit = Review.objects.filter(user=self.user, content_type=self.content_type, object_id=self.object_id).aggregate(last_visit=Max('visit_count'))['last_visit']
        # 이전 방문이 있다면 visit_count 증가
        self.visit_count = (last_visit or 0) + 1
        super().save(*args, **kwargs)  # 기존 save() 메서드 호출하여 저장

    def __str__(self):
        return f"{self.place} - {self.rating} - 방문 {self.visit_count}회"

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_images/')

    def __str__(self):
        return f"Image for {self.review.place} review"