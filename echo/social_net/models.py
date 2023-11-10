from django.db import models
from .accounts import CustomUser as User
from resources import *
from django.urls import reverse
from django.core.mail import send_mail
from django.db.models.functions import Coalesce
from django.db.models import Sum


class Post(models.Model):
    """
    Модель для представления постов.

    Поля:
        author (ForeignKey): Автор поста.
        date_created (DateTimeField): Дата создания поста.
        category (CharField): Категория поста.
        header (CharField): Заголовок поста.
        content (TextField): Содержание поста.
        image1 (ImageField): Изображение к посту (необязательное).
        post_rating (IntegerField): Рейтинг поста.

    Методы:
        get_category_display_ru(): Возвращает название категории на русском языке.
        like(): Увеличивает рейтинг поста на единицу.
        preview(): Возвращает превью содержания поста (первые 100 символов).
        __str__(): Возвращает строковое представление поста в формате "Заголовок: Превью содержания".

    """

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    CATEGORY_CHOICES = (
        ('MV', 'Кино'),
        ('SP', 'Спорт'),
        ('CL', 'Культура'),
        ('FD', 'Еда'),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    header = models.CharField(max_length=100)
    content = models.TextField()
    image1 = models.ImageField(blank=True)
    post_rating = models.IntegerField(default=0)

    def get_category_display_ru(self):
        """
        Возвращает название категории на русском языке.
        """
        category_choices = dict(self.CATEGORY_CHOICES)
        return category_choices.get(self.category, '')

    def like(self):
        """
        Увеличивает рейтинг поста на единицу.
        """
        self.post_rating += 1
        self.save()

    def preview(self):
        """
        Возвращает превью содержания поста (первые 100 символов).
        """
        return self.content[:100] + '...' if len(self.content) > 100 else self.content

    def __str__(self):
        """
        Возвращает строковое представление поста в формате "Заголовок: Превью содержания".
        """
        return f'{self.header}: {self.content[:100]}'


class Comment(models.Model):
    """
    Модель для представления комментариев к постам.

    Поля:
        comment_post (ForeignKey): Пост, к которому оставлен комментарий.
        user (ForeignKey): Пользователь, оставивший комментарий.
        text (TextField): Текст комментария.
        time_create (DateTimeField): Дата и время создания комментария.
        comment (BooleanField): Флаг, указывающий, является ли комментарий ответом на другой комментарий.

    Методы:
        send_email(): Отправляет уведомление по электронной почте об отклике на публикацию.
        __str__(): Возвращает текст комментария.
    """

    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    comment = models.BooleanField(default=False)

    def send_email(self):
        """
        Отправляет уведомление по электронной почте об отклике на публикацию.
        """
        subject = 'Отклик на публикацию'
        message = f'Здравствуйте! На вашу публикацию "{self.comment_post.header}" появился новый отклик. С уважением, Echo.'
        from_email = admin_email
        recipient_list = [self.comment_post.author.email]

        send_mail(subject, message, from_email, recipient_list)

    def __str__(self):
        """
        Возвращает текст комментария.
        """
        return self.text
