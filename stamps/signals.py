from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from reviews.models import Review
from .models import StampedPlace
from baseplace.models import BasePlace

User = get_user_model()

# 1. 리뷰가 생성될 때 방문 횟수 증가하기
@receiver(post_save, sender=Review)
def increase_visit_count(sender, instance, created, **kwargs):
    if created:  # 리뷰가 처음 생성된 경우에만
        place = instance.place  # Review의 GenericForeignKey 필드에 연결된 place
        user = instance.user

        # 해당 유저와 place에 대한 StampPlace 객체를 가져오거나 생성
        stamp, created = StampedPlace.objects.get_or_create(user=user, place_id=place.place_id)
        
        # 방문 횟수 증가
        stamp.visit_count += 1
        stamp.save()

# 2. 회원가입 시 모든 StampPlace 생성
@receiver(post_save, sender=User)
def create_stampplaces_for_new_user(sender, instance, created, **kwargs):
    if created:  # 유저가 처음 생성된 경우에만
        # 모든 BasePlace 하위 클래스의 인스턴스를 가져옴
        all_places = BasePlace.objects.all()

        # 각 장소에 대해 StampPlace를 생성 (방문 횟수 0으로 초기화)
        for place in all_places:
            StampedPlace.objects.create(user=instance, place_id=place.place_id, visit_count=0)
