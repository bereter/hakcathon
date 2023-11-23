from rest_framework import serializers
from accounts.models import CustomUser


class VKAuthSerializer(serializers.Serializer):
    """
    Сериализатор для аутентификации через ВКонтакте.

    Поля:
        vkontakte_id (CharField): Идентификатор пользователя в ВКонтакте.
    """
    vkontakte_id = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser.

    Поля:
        id (IntegerField): Уникальный идентификатор пользователя.
        username (CharField): Имя пользователя (логин).
        email (EmailField): Email пользователя.
        photo (ImageField): Фотография пользователя.
        date_birth (DateTimeField): Дата рождения пользователя.
        user_raiting (IntegerField): Рейтинг пользователя.
        vkontakte_id (CharField): Идентификатор пользователя в ВКонтакте.
        verification_code (IntegerField): Код верификации пользователя.
        about (CharField): Описание пользователя.

    Метаданные:
        model (CustomUser): Модель, для которой создается сериализатор.
        fields (tuple): Перечень полей, включаемых в сериализацию.
    """
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'photo', 'date_birth', 'user_raiting', 'vkontakte_id', 'verification_code',
            'about'
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.

    Поля:
        username (CharField): Имя пользователя (логин).
        email (EmailField): Email пользователя.
        password (CharField): Пароль пользователя.
        vkontakte_id (CharField): Идентификатор пользователя в ВКонтакте.

    Метаданные:
        model (CustomUser): Модель, для которой создается сериализатор.
        fields (tuple): Перечень полей, включаемых в сериализацию.
        extra_kwargs (dict): Дополнительные аргументы для определенных полей.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'vkontakte_id')
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа пользователя.

    Поля:
        username (CharField): Имя пользователя (логин).
        password (CharField): Пароль пользователя (для записи).

    Метаданные:
        model (CustomUser): Модель, для которой создается сериализатор.
        fields (tuple): Перечень полей, включаемых в сериализацию.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class VKAuthUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя, созданного через ВКонтакте.

    Поля:
        vkontakte_id (CharField): Идентификатор пользователя в ВКонтакте.

    Метаданные:
        model (CustomUser): Модель, для которой создается сериализатор.
        fields (tuple): Перечень полей, включаемых в сериализацию.
    """
    class Meta:
        model = CustomUser
        fields = ('vkontakte_id',)
