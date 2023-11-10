from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import AbstractUser
from social_net.models import Post


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.

    Поля:
        username (CharField): Имя пользователя (логин).
        password (CharField): Хэшированный пароль пользователя.
        email (EmailField): Email пользователя.
        verification_code (IntegerField): Код верификации пользователя. (пользовательская добавка)
        photo (ImageField): Фотография пользователя.
        date_birth (DateTimeField): Дата рождения пользователя.
        user_raiting (IntegerField): Рейтинг пользователя.
        vkontakte_id (CharField): Идентификатор пользователя в ВКонтакте.

    Методы:
        link_vk_account(vkontakte_id): Связывает аккаунт пользователя с указанным ID ВКонтакте.
        create_user_from_vk(vkontakte_id, username, email=None): Создает пользователя на основе данных из
            аккаунта ВКонтакте и автоматически связывает его с указанным ID ВКонтакте.
        update_rating(): Обновляет рейтинг пользователя на основе рейтинга его постов.
        __str__(): Возвращает строковое представление пользователя (имя).
    """

    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    user_raiting = models.IntegerField(default=0)
    vkontakte_id = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name="ID ВКонтакте")
    verification_code = models.IntegerField(default=0)

    def link_vk_account(self, vkontakte_id):
        """
                Связывает аккаунт пользователя с указанным ID ВКонтакте.

                :param vkontakte_id: Идентификатор пользователя в ВКонтакте.
        """

        self.vkontakte_id = vkontakte_id
        self.save()

    @classmethod
    def create_user_from_vk(cls, vkontakte_id, username, email=None):
        """
                Создает пользователя на основе данных из аккаунта ВКонтакте
                и автоматически связывает его с указанным ID ВКонтакте.

                :param vkontakte_id: Идентификатор пользователя в ВКонтакте.
                :param username: Имя пользователя.
                :param email: Email пользователя (по умолчанию None).
                :return: Созданный пользователь.
        """

        user = cls.objects.create(username=username, email=email)
        user.link_vk_account(vkontakte_id)
        return user

    def update_rating(self):
        """
                Обновляет рейтинг пользователя на основе рейтинга его постов.
        """

        post_rating = Post.objects.filter(author=self).aggregate(p_r=Coalesce(Sum('post_rating'), 0))['p_r']
        self.user_raiting = post_rating
        self.save()

    def __str__(self):
        return self.username
