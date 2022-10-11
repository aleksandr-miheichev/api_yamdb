from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import CustomUser


class UsersSerializer(serializers.ModelSerializer):
    username = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = CustomUser
        fields = ('username',
            'first_name',
            'second_name',
            'email',
            'conformation_code',
            'role',
            'bio',
        )
