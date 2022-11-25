from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)  # jwt
from users import views


urlpatterns = [  # jwt
    path('api/token/', views.CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),  # 로그인
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),  # refesh
    path('<int:user_pk>/', views.UserProfileView.as_view(),
         name="UserView"),  # 유저 정보 조회
    path('signup/', views.UserSignView.as_view(), name="UserView"),  # 회원가입

]
