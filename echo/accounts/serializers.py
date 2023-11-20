from rest_framework import serializers

from accounts.models import CustomUser


class VKAuthSerializer(serializers.Serializer):
    vkontakte_id = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'photo', 'date_birth', 'user_raiting', 'vkontakte_id', 'verification_code',
            'about')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'vkontakte_id')
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class VKAuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('vkontakte_id',)
