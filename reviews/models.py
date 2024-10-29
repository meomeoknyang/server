from django.db import models
from restaurants.models import Restaurant
from django.conf import settings

class Keyword(models.Model):
    description = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.description


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)  # 작성자 필드
    rating = models.PositiveSmallIntegerField()  # 별점 (1~5)
    comment = models.TextField(blank=True, null=True)  # 리뷰 코멘트
    keywords = models.ManyToManyField(Keyword, related_name='reviews')  # 중복 선택 가능한 키워드
    created_at = models.DateTimeField(auto_now_add=True)  # 리뷰 작성 날짜

    def __str__(self):
        return f"{self.restaurant.name} - {self.rating}"

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_images/')

    def __str__(self):
        return f"Image for {self.review.restaurant.name} review"