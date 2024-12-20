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
from rest_framework.permissions import IsAuthenticated

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        place_type = self.kwargs['place_type']
        place_id = self.kwargs['place_id']

        if place_type == 'restaurant':
            content_type = ContentType.objects.get(app_label='restaurants', model='restaurant')
        elif place_type == 'cafe':
            content_type = ContentType.objects.get(app_label='cafe', model='cafe')
        else:
            raise ValueError("Invalid 'place_type'. Must be 'restaurant' or 'cafe'.")

        return Review.objects.filter(content_type=content_type, object_id=place_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'place_type': self.kwargs['place_type'],
            'place_id': self.kwargs['place_id']
        })
        return context
    
    def list(self, request, *args, **kwargs):
        """
        GET 요청을 처리 (특정 장소의 리뷰 조회)
        """
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
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
                data={"error": str(e)}
            )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'place_type': self.kwargs['place_type'],
            'place_id': self.kwargs['place_id']
        })
        return context
        
# 특정 사용자가 작성한 리뷰 전체 조회
class UserReviewsView(APIView):
    def get(self, request, user_id):
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            reviews = Review.objects.filter(user=user)
            serializer = ReviewSerializer(reviews, many=True)
            return CustomResponse(
                status_text="success",
                message="사용자의 리뷰 목록을 성공적으로 조회했습니다.",
                code=status.HTTP_200_OK,
                data=serializer.data
            )
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
                data=str(e)
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
                data=str(e)
            )

class ReviewCountView(APIView):
    permission_classes = [IsAuthenticated]  # 유저 인증 필요

    def get(self, request):
        try:
            # 현재 인증된 사용자 가져오기
            user = request.user
            
            # 해당 사용자의 리뷰 수 조회
            review_count = Review.objects.filter(user=user).count()
            data = review_count
            return CustomResponse(
                status_text="success",
                message="리뷰 개수를 성공적으로 조회했습니다.",
                code=status.HTTP_200_OK,
                data=data
            )

        except Exception as e:
            return CustomResponse(
                status_text="error",
                message="리뷰 조회 중 알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=str(e)
            )