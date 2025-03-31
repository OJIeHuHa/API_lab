from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "gender", "date_of_birth"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "gender", "date_of_birth"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
