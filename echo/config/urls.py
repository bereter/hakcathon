"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from social_net.views import *
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/post_list/', PostsViewSet.as_view({'get': 'list'})),
    path('api/v1/profile/<int:pk>/', ProfileViewSet.as_view({'get': 'retrieve', 'put': 'partial_update'})),
    # path('api/v1/post_list_category/', CategoryPostsViewSet.as_view({'get': 'list'})),
    # path('', include('accounts.urls')),
    # path('sign/', include('sign.urls')),
    # #или
    # path('sign/', 'views.register', name='sign'),
    # path('accounts/', include('allauth.urls')),
    # path('profile/', include('profile.urls')),
    # # или
    # path('profile/', 'views.profile', name='profile'),
    # path('', include('social_net.urls')),

]
