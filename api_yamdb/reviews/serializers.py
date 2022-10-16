from rest_framework import serializers

from .models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
        )


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'confirmation_code',
        )


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role',
        )
