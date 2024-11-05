from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from meomeoknyang.responses import CustomResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView

class UserRegistrationView(APIView):

    @swagger_auto_schema(request_body=CustomUserSerializer)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(
                    status_text="success",
                    message="회원가입이 성공적으로 완료되었습니다.",
                    code=status.HTTP_201_CREATED,
                    data=serializer.data
                )
            return CustomResponse(
                status_text="error",
                message="회원가입에 실패했습니다.",
                code=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        except Exception as e:
            return CustomResponse(
                status_text="error",
                message="알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"error": str(e)}
                # data = None
            )
# class UserDetailView(generics.RetrieveAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     lookup_field = 'id'  # URL에서 사용자의 ID를 기준으로 조회

# 현재 로그인된 사용자 정보 반환
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 접근 가능

    def get(self, request):
        try:
            user = request.user
            serializer = CustomUserSerializer(user)
            return CustomResponse(
                status_text="success",
                message="프로필 정보 조회 성공",
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
            # 알 수 없는 예외 처리
            return CustomResponse(
                status_text="error",
                message="알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                # data={"error": str(e)}
                data=None
            )
        
    #닉네임 업데이트
    @swagger_auto_schema(request_body=CustomUserSerializer)
    def patch(self, request):
        try:
            user = request.user
            data = request.data

            # 닉네임 업데이트
            if 'nickname' in data:
                user.nickname = data['nickname']

            user.save()
            return CustomResponse(
                status_text="success",
                message="프로필 정보가 업데이트되었습니다.",
                code=status.HTTP_200_OK,
                data={"nickname": user.nickname}
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
                message="알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None
            )
        
# # 닉네임 업데이트
# class UserUpdateView(APIView):
#     permission_classes = [IsAuthenticated]  # 로그인된 사용자만 접근 가능

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            response_data = serializer.validated_data
            return CustomResponse(
                status_text=response_data['status'],
                message=response_data['message'],
                code=response_data['code'],
                data=response_data['data']
            )
        except Exception as e:
            # 인증 오류에 대한 메시지 처리
            if str(e) == "No active account found with the given credentials":
                return CustomResponse(
                    status_text="error",
                    message="아이디 또는 비밀번호가 올바르지 않습니다.",
                    code=status.HTTP_401_UNAUTHORIZED,
                    data=None
                )
            return CustomResponse(
                status_text="error",
                message="로그인 중 알 수 없는 오류가 발생했습니다.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"error": str(e)}
            )
