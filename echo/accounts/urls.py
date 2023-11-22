from django.urls import path
from .views import UserRegistrationView, UserLoginView, VKAuthView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('vk-auth/', VKAuthView.as_view(), name='vk-auth'),
]
