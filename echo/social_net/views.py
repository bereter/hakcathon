from django.shortcuts import render
from rest_framework import generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Post
from accounts.models import CustomUser as User
from .serializers import PostsSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly


class PaginationAPIList(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['postCategory__categories', 'author']  # Обновлено для связанного поля postCategory
    ordering_fields = ['postCategory__categories', 'date_created']  # Обновлено для связанного поля postCategory
    ordering = ['-_rating', '-date_created']
    pagination_class = PaginationAPIList
    # permission_classes = (IsAuthenticatedOrReadOnly, )


# class CategoryPostsViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['postCategory__categories']  # Обновлено для связанного поля postCategory


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)
