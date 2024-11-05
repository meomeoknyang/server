# reviews/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Review
from .serializers import ReviewSerializer
from users.models import CustomUser
from meomeoknyang.responses import CustomResponse

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return CustomResponse(
                status_text="success",
                message="리뷰가 성공적으로 생성되었습니다.",
                code=status.HTTP_201_CREATED,
                data=response.data
            )
        except Exception as e:
            return CustomResponse(
                status_text="error",
                message="리뷰 생성 중 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None
            )
        
# 특정 사용자가 작성한 리뷰 전체 조회
class UserReviewsView(APIView):
    def get(self, request, user_id):
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            reviews = Review.objects.filter(user=user)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return CustomResponse(
                status_text="error",
                message="사용자를 찾을 수 없습니다.",
                code=status.HTTP_404_NOT_FOUND,
                data=None
            )
        except Exception as e:
            return CustomResponse(
                status_text="error",
                message="리뷰 조회 중 알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None
            )
    
# 특정 장소(Restaurant or Cafe)의 리뷰 전체 조회
class PlaceReviewsView(APIView):
    def get(self, request, place_type, place_id):
        try:
            # ContentType을 이용하여 place_type을 모델로 변환
            if place_type == 'restaurant':
                content_type = ContentType.objects.get(app_label='restaurants', model='restaurant')
            elif place_type == 'cafe':
                content_type = ContentType.objects.get(app_label='cafe', model='cafe')
            else:
                return CustomResponse(
                    status_text="error",
                    message="유효하지 않은 장소 타입입니다.",
                    code=status.HTTP_400_BAD_REQUEST,
                    data=None
                )
            
            # 특정 장소에 대한 리뷰 필터링
            reviews = Review.objects.filter(content_type=content_type, object_id=place_id)
            serializer = ReviewSerializer(reviews, many=True)
            return CustomResponse(
                status_text="success",
                message="특정 장소의 리뷰 목록을 성공적으로 조회했습니다.",
                code=status.HTTP_200_OK,
                data=serializer.data
            )
        
        except ContentType.DoesNotExist:
            return CustomResponse(
                status_text="error",
                message="해당 장소 타입을 찾을 수 없습니다.",
                code=status.HTTP_404_NOT_FOUND,
                data=None
            )
        
        except Exception as e:
            return CustomResponse(
                status_text="error",
                message="리뷰 조회 중 알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None
            )


# 특정 리뷰 상세 조회
class ReviewDetailView(APIView):
    def get(self, request, review_id):
        try:
            review = get_object_or_404(Review, id=review_id)
            serializer = ReviewSerializer(review)
            return CustomResponse(
                status_text="success",
                message="리뷰 상세 정보를 성공적으로 조회했습니다.",
                code=status.HTTP_200_OK,
                data=serializer.data
            )
        except Review.DoesNotExist:
            return CustomResponse(
                status_text="error",
                message="리뷰를 찾을 수 없습니다.",
                code=status.HTTP_404_NOT_FOUND,
                data=None
            )
        except Exception as e:
            return CustomResponse(
                status_text="error",
                message="리뷰 조회 중 알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None
            )
