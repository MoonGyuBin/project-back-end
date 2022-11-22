from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView   # jwt
)


# Create your views here.

# 회원가입
class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료"},)
        else:
            return Response({"message":f"${serializer.errors}"})

# jwt 토큰 커스터마이징 
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

