from django.urls import path
from .views import UserRegistrationView, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path('<int:id>/', UserDetailView.as_view(), name='user-detail'),  # 사용자 ID로 조회
    path('register/', UserRegistrationView.as_view(), name='user-register'),  # 회원가입 엔드포인트
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 로그인 엔드포인트
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 토큰 갱신 엔드포인트

    path('profile/', UserProfileView.as_view(), name='user-profile'),  # 현재 유저 정보 조회
    # path('profile/update/', UserUpdateView.as_view(), name='user-update'),  # 유저 정보 수정
]