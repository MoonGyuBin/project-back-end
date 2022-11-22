from rest_framework import serializers
from users.models import User 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # jwt 토큰 커스터마이징



# 회원가입
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data) 
        
        password = user.password 
        
        user.set_password(password) 
      
        user.save() 
        return user

    
    def update(self, instance, validated_data):
        user = super().create(validated_data) 
        password = user.password 
        user.set_password(password) 
        user.save() 
        return user




# jwt 이메일 
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email # 이메일
        return token