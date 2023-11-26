from rest_framework import serializers
from accounts.models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


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

    def authenticate(self, **kwargs):
        """
        Аутентификация пользователя на основе предоставленных данных.
        """
        username = kwargs['username']
        password = kwargs['password']

        user = CustomUser.objects.get(username=username)

        if user.check_password(password):
            return user
        return None


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
        fields = ('username', 'password')
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

    def validate(self, data):
        """
        Проверка введенных данных.

        :param data: Словарь с данными для валидации.
        :return: Валидированные данные.
        """
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            data['user'] = user
        else:
            raise serializers.ValidationError("Неверные учетные данные")

        return data

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
