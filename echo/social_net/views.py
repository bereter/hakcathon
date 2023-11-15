from django.shortcuts import render
from rest_framework import generics
from .models import Post, Profile
from .serializers import PostSerializer, ProfileSerializer


class PostListAPIViev(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ProfileAPIViev(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
