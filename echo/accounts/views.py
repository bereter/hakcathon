from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import CustomUserSerializer, UserRegistrationSerializer, UserLoginSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    API-представление для регистрации нового пользователя.

    Методы:
        perform_create(serializer): Создает нового пользователя и сохраняет его в базе данных.

    Поля:
        queryset (QuerySet): Набор данных для запроса всех пользователей.
        serializer_class (UserRegistrationSerializer): Сериализатор для данных пользователя.
        permission_classes (tuple): Кортеж с классами разрешений (в данном случае, разрешено всем).
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        password = serializer.validated_data.get('password')
        user.set_password(password)
        user.save()


class UserLoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(UserLoginAPIView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user

        # Добавляем информацию о входе пользователя
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,  # добавьте другие необходимые поля
        }

        return Response({'token': token.key, 'user': user_data})



class VKAuthView(APIView):
    """
    API-представление для аутентификации через ВКонтакте.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Ваша логика обработки запроса для аутентификации через ВКонтакте
        # ...

        # Пример: получение vkontakte_id из запроса
        vkontakte_id = request.data.get('vkontakte_id')

        # Пример: создание пользователя или получение существующего
        user, created = CustomUser.objects.get_or_create(vkontakte_id=vkontakte_id)

        # Пример: сохранение пользователя, если он новый
        if created:
            user.save()

        # Пример: создание или получение токена доступа
        token, created = Token.objects.get_or_create(user=user)

        # Пример: создание сериализатора пользователя
        user_serializer = CustomUserSerializer(user)

        # Пример: возврат ответа с токеном и данными пользователя
        return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
