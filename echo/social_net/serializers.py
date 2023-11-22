from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['author', 'photo']


class PostsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Post
        depth = 1
        fields = ['user', 'date_created', 'categories', 'header', 'photo', 'content', 'estimation',
                  'comment']


class PhotoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['photo']


class ProfileSerializer(serializers.ModelSerializer):
    post_user = PhotoPostSerializer(many=True)

    class Meta:
        model = Profile
        depth = 1
        fields = ['author', 'photo', 'description', 'post_user', 'subscribers']