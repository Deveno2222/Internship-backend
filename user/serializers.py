from rest_framework.serializers import ModelSerializer, Serializer
from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class CustomUserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id", "email", "username", "role")
        
        
        
class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "role", "password")
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }
        
    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            role=validated_data["role"]
        )
        user.set_password(validated_data["password"])  # хэшируем пароль
        user.save()
        return user
    
    
class LoginUserSerializer(Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials!")
    
    
    