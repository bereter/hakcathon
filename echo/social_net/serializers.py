from rest_framework import serializers
from .models import Post
from accounts.models import CustomUser as Profile


class PostsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    comment_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ['author', 'date_created', 'postCategory', 'header', 'photo', 'content', 'estimation', 'comment_set']


class PhotoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['photo']


class UserSerializer(serializers.ModelSerializer):
    post_user = PostsSerializer(many=True)

    class Meta:
        model = Profile
        fields = ['username', 'photo', 'about', 'subscribers', 'post_user']
