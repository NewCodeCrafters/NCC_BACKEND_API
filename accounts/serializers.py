from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "role", "slug"]
        extra_kwargs = {
            "password": {"write_only": True},
            "slug": {"read_only": True},
            "email": {"required": True},
        }

    def validate_role(self, value):
        if value not in ["admin", "teacher", "student"]:
            raise serializers.ValidationError("Invalid role selected.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"],
            username=validated_data["email"],
        )
        return user


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users (excluding password)."""

    class Meta:
        model = User
        fields = ["slug", "email", "role"]
