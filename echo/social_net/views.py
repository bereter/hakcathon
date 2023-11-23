from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostsSerializer, UserSerializer, PhotoPostSerializer
from .permissions import IsOwnerOrReadOnly


class PaginationAPIList(PageNumberPagination):
    """
    Пагинация для API-списка.

    Поля:
        page_size (int): Количество элементов на странице.
        page_size_query_param (str): Параметр запроса для указания количества элементов на странице.
        max_page_size (int): Максимальное количество элементов на странице.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostsViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Post.

    Поля:
        queryset (QuerySet): Набор данных для запросов.
        serializer_class (serializer): Сериализатор для модели.
        filter_backends (list): Список используемых фильтров.
        filterset_fields (list): Поля для фильтрации.
        ordering_fields (list): Поля для сортировки.
        ordering (list): Порядок сортировки.
        pagination_class (PaginationAPIList): Класс пагинации.

    Права доступа:
        IsAuthenticatedOrReadOnly: Только для аутентифицированных пользователей.

    Методы:
        list(): Возвращает список постов.
        create(): Создает новый пост.
        retrieve(): Возвращает пост по идентификатору.
        update(): Обновляет пост.
        partial_update(): Обновляет часть поста.
        destroy(): Удаляет пост.
    """
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['postCategory__categories', 'author']
    ordering_fields = ['postCategory__categories', 'date_created']
    ordering = ['-_rating', '-date_created']
    pagination_class = PaginationAPIList
    # permission_classes = (IsAuthenticatedOrReadOnly, )


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet для профиля пользователя.

    Поля:
        queryset (QuerySet): Набор данных для запросов.
        serializer_class (serializer): Сериализатор для модели.
        permission_classes (tuple): Кортеж с классами разрешений.

    Права доступа:
        IsOwnerOrReadOnly: Доступ только владельцу или в режиме "только чтение".

    Методы:
        list(): Возвращает список пользователей.
        create(): Создает нового пользователя.
        retrieve(): Возвращает пользователя по идентификатору.
        update(): Обновляет пользователя.
        partial_update(): Обновляет часть пользователя.
        destroy(): Удаляет пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)



# class CategoryPostsViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['postCategory__categories']  # Обновлено для связанного поля postCategory


