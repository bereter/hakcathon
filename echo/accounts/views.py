from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SignUpAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'pk': user.pk}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificationAPIView(APIView):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['verification_code'] == user.verification_code:
                user.is_active = True
                user.save()
                return Response({'detail': 'Email успешно подтвержден.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Неверный код подтверждения.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
