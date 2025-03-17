from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id', 'role']  # Prevent users from modifying their role

    def create(self, validated_data):
        # Only staff/admin can create users
        if not self.context['request'].user.is_staff:
            raise serializers.ValidationError("Only staff/admin can create users.")
        return User.objects.create_user(**validated_data)
