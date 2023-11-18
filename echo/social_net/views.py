from django.shortcuts import render
from rest_framework import generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Post, Profile
from .serializers import PostsSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class PaginationAPIList(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['categories', 'user']
    ordering_fields = ['categories', 'date_created']
    ordering = ['-date_created']
    pagination_class = PaginationAPIList
    # permission_classes = (IsAuthenticatedOrReadOnly, )


# class CategoryPostsViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['categories']


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
