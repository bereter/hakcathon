from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import CustomUserSerializer, UserRegistrationSerializer, UserLoginSerializer, VKAuthSerializer, \
    VKAuthUserSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = CustomUserSerializer(user)  # Используем CustomUserSerializer здесь
        return Response({'token': token.key, 'user': user_serializer.data})


class VKAuthView(generics.CreateAPIView):
    serializer_class = VKAuthSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        vkontakte_id = serializer.validated_data['vkontakte_id']
        user, created = CustomUser.objects.get_or_create(vkontakte_id=vkontakte_id)

        if created:
            user.save()

        token, created = Token.objects.get_or_create(user=user)
        user_serializer = CustomUserSerializer(user)  # Используем CustomUserSerializer здесь

        return Response({'token': token.key, 'user': user_serializer.data})
