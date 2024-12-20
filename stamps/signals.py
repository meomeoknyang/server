from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from reviews.models import Review
from .models import StampedPlace
from cafe.models import Cafe
from restaurants.models import Restaurant
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

# 1. 리뷰가 생성될 때 방문 횟수 증가하기
@receiver(post_save, sender=Review)
def increase_visit_count(sender, instance, created, **kwargs):
    if created:  # 리뷰가 처음 생성된 경우에만
        # place = instance.place  # Review의 GenericForeignKey 필드에 연결된 place
        user = instance.user
        object_id = instance.object_id  # 바로 object_id를 사용
        content_type = instance.content_type
        # content_type과 object_id를 사용하여 StampedPlace 조회
        stamp, created = StampedPlace.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=object_id
        )
       # visit_count 증가
        if not created:
            stamp.visit_count += 1
            stamp.save()

# 2. 회원가입 시 모든 StampPlace 생성
@receiver(post_save, sender=User)
def create_stampplaces_for_new_user(sender, instance, created, **kwargs):
    if created:  # 유저가 처음 생성된 경우에만
        # 모든 BasePlace 하위 클래스의 인스턴스를 가져옴
        all_places = list(Cafe.objects.all()) + list(Restaurant.objects.all())

        # 각 장소에 대해 StampedPlace를 생성 (방문 횟수 0으로 초기화)
        for place in all_places:
            content_type = ContentType.objects.get_for_model(place)
            StampedPlace.objects.create(
                user=instance,
                content_type=content_type,  # content_type 추가
                object_id=place.place_id,   # object_id 추가
                visit_count=0,
                average_price=place.average_price,          # 기본값 설정
                distance_from_gate=place.distance_from_gate  # 기본값 설정
            )

# @receiver(post_save, sender=Cafe)
# def create_stampedplace_for_cafe(sender, instance, created, **kwargs):
#     if created:
#         StampedPlace.objects.get_or_create(
#                 content_type=ContentType.objects.get_for_model(Cafe),
#                 object_id=instance.place_id,
#                 defaults={'visit_count': 0}
#             )

# # Restaurant 생성 시 StampedPlace 생성
# @receiver(post_save, sender=Restaurant)
# def create_stampedplace_for_restaurant(sender, instance, created, **kwargs):
#     if created:
#         StampedPlace.objects.get_or_create(
#                 content_type=ContentType.objects.get_for_model(Restaurant),
#                 object_id=instance.place_id,
#                 defaults={'visit_count': 0}
#             )