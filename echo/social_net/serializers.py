from rest_framework import serializers
from .models import Post
from accounts.models import CustomUser as Profile


class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        depth = 1
        fields = ['author', 'date_created', 'postCategory', 'header', 'image1', 'content', 'estimation', 'rating']


class PhotoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'image1']


class UserSerializer(serializers.ModelSerializer):
    post_user = PhotoPostSerializer(many=True)

    class Meta:
        model = Profile
        depth = 1
        fields = ['username', 'photo', 'about', 'subscribers', 'post_user']
