from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.db.models.functions import Coalesce


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
        about (CharField): Краткое описание пользователя.
        subscribers (ManyToManyField): Подписчики пользователя.

    Методы:
        link_vk_account(vkontakte_id): Связывает аккаунт пользователя с указанным ID ВКонтакте.
        create_user_from_vk(vkontakte_id, username, email=None): Создает пользователя на основе данных из
            аккаунта ВКонтакте и автоматически связывает его с указанным ID ВКонтакте.
        update_rating(): Обновляет рейтинг пользователя на основе рейтинга его постов.
        __str__(): Возвращает строковое представление пользователя (имя).
    """

    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    vkontakte_id = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name="ID ВКонтакте")
    about = models.CharField(max_length=150, blank=True, null=True, unique=True, verbose_name="О себе")
    subscribers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='subscriptions',
                                         verbose_name='Подписчики')
    verification_code = models.IntegerField(default=0)
    user_raiting = models.IntegerField(default=0)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='customuser_groups',  # Добавлено это поле
        related_query_name='group',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_user_permissions',  # Добавлено это поле
        related_query_name='user_permission',
    )

    def update_rating(self):
        """
        Обновляет рейтинг пользователя на основе рейтинга его постов.
        """
        post_rating = self.post_user.aggregate(p_r=Coalesce(Sum('post_rating'), 0))['p_r']
        self.user_raiting = post_rating
        self.save()

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
        Создает пользователя на основе данных из аккаунта ВКонтакте и автоматически связывает его с указанным ID ВКонтакте.

        :param vkontakte_id: Идентификатор пользователя в ВКонтакте.
        :param username: Имя пользователя (логин).
        :param email: Email пользователя.
        :return: Новый объект пользователя.
        """
        user = cls.objects.create(username=username, email=email)
        user.link_vk_account(vkontakte_id)
        return user

    def __str__(self):
        """
        Возвращает строковое представление пользователя (имя).

        :return: Строковое представление пользователя.
        """
        return self.username
