from rest_framework import serializers
from .models import Post
from accounts.models import CustomUser as Profile
from rest_framework import serializers
from .models import Post


class PostsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.

    Поля:
        author (CustomUser): Автор поста (связь с CustomUser).
        date_created (DateTimeField): Дата создания поста.
        postCategory (Category): Категории поста (связь с Category).
        header (CharField): Заголовок поста.
        image1 (ImageField): Изображение поста.
        content (TextField): Содержимое поста.
        estimation (IntegerField): Оценка поста (от 1 до 5).
        rating (IntegerField): Рейтинг поста (количество комментариев).

    Мета:
        model (Post): Используемая модель.
        depth (int): Глубина связанных моделей для сериализации.
        fields (list): Список полей для сериализации.
    """
    class Meta:
        model = Post
        depth = 1
        fields = ['author', 'date_created', 'postCategory', 'header', 'image1', 'content', 'estimation', 'rating']


class PhotoPostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изображения поста.

    Поля:
        id (int): Идентификатор поста.
        image1 (ImageField): Изображение поста.

    Мета:
        model (Post): Используемая модель.
        fields (list): Список полей для сериализации.
    """
    class Meta:
        model = Post
        fields = ['id', 'image1']


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.

    Поля:
        username (CharField): Имя пользователя.
        photo (ImageField): Фотография пользователя.
        about (CharField): О себе.
        subscribers (ManyToManyField): Подписчики пользователя.
        post_user (PhotoPostSerializer): Сериализатор для изображений постов пользователя.

    Мета:
        model (Profile): Используемая модель.
        depth (int): Глубина связанных моделей для сериализации.
        fields (list): Список полей для сериализации.
    """
    post_user = PhotoPostSerializer(many=True)

    class Meta:
        model = Profile
        depth = 1
        fields = ['username', 'photo', 'about', 'subscribers', 'post_user']
