from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Post, Profile
from .serializers import PostSerializer, ProfileSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
