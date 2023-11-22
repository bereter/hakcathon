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
from rest_framework import permissions
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import UserRegistrationView, UserLoginView, VKAuthView
from social_net.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('vk-auth/', VKAuthView.as_view(), name='vk-auth'),
    path('api/v1/post_list/', PostsViewSet.as_view({'get': 'list'})),
    path('api/v1/profile/<int:pk>/', ProfileViewSet.as_view({'get': 'retrieve', 'put': 'partial_update'})),
    re_path(r'^swagger(\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
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
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
