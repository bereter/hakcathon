from rest_framework import serializers
from .models import *


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         depth = 1
#         fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        depth = 1
        fields = ['user', 'date_created', 'categories', 'header', 'photo', 'content', 'estimation', 'comment']


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