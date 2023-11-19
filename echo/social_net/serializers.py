from rest_framework import serializers
from .models import *
from .models import Post, Category, Comment


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         depth = 1
#         fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        depth = 1
        fields = [
            'user',
            'date_created',
            'categories',
            'header',
            'content',
        ]

    # переопределение метода post (передача авторизованного пользователя и его связь с категориями
    def create(self, validated_data, **kwargs):
        # получение данных публикации из валидатора
        categories = validated_data.pop('categories')
        user = validated_data.pop('user')
        header = validated_data.pop('header')
        content = validated_data.pop('content')
        # создание публикации
        post = Post.objects.create(header=header, content=content, user=user)
        # if categories:
        #     post.categories.set(categories)

        return post


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'url',
            'id',
            'name',
        ]

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), allow_null=True)

    class Meta:
        model = Comment
        depth = 1
        fields = [
            'url',
            'id',
            'text',
            'post',
        ]


class PhotoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['photo']


class ProfileSerializer(serializers.ModelSerializer):
    post_user = PhotoPostSerializer(many=True)

    class Meta:
        #model = Profile
        depth = 1
        fields = ['author', 'photo', 'description', 'post_user']
