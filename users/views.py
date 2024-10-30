from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 성공적으로 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'  # URL에서 사용자의 ID를 기준으로 조회

# 현재 로그인된 사용자 정보 반환
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 접근 가능

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
# 닉네임 업데이트
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 접근 가능

    def patch(self, request):
        user = request.user
        data = request.data

        # 닉네임 업데이트
        if 'nickname' in data:
            user.nickname = data['nickname']

        user.save()
        return Response({"message": "프로필 정보가 업데이트되었습니다."}, status=status.HTTP_200_OK)