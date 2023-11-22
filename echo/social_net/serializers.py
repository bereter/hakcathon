from rest_framework import serializers
from .models import Post
from accounts.models import CustomUser as Profile


class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['author', 'date_created', 'postCategory', 'header', 'image1', 'content', 'post_rating']


class PhotoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['photo']


class UserSerializer(serializers.ModelSerializer):
    post_user = PostsSerializer(many=True)

    class Meta:
        model = Profile
        fields = ['username', 'photo', 'about', 'subscribers', 'post_user']
