from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # jwt 토큰 커스터마이징

# 회원가입


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):

        if len(data.get("email", "")) < 8:
            raise serializers.ValidationError(
                detail={"error": "이메일이 8글자 이상이어야 합니다."}
            )
        elif len(data.get("password", "")) < 3:
            raise serializers.ValidationError(
                detail={"error": "비밀번호는 3글자 이상이어야 합니다."}
            )

        return data

    def create(self, validated_data):
        password = validated_data.pop("password", "")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()

        return instance

# jwt 이메일


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email  # 이메일
        return token
