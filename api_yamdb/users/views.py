from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator   
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User
from .serializers import *


@api_view(['POST'])
def registration_API_view(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    users = User.objects.filter(username=username)
    if users.exists():
        return Response(
            data={
                'error': 'Данный пользователь уже зарегестрирован.',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, email=email)
    user.save()

    token = default_token_generator.make_token(user)
    try:
        send_mail(
            f'Token',
            f'{token}',
            'Cuencaldd@ya.ru',
            [email],
            fail_silently=False,
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    except:
        user.delete()
        return Response(
            data={
                'error': 'Ошибка отправки кода подтверждения!',
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def take_confirmation_code_view(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(
            data={
                'error': 'Неподходящий токен'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    refresh_token = RefreshToken.for_user(user)
    return Response(
        data={
            'refresh':str(refresh_token),
            'access': str(refresh_token.access_token)
        },
        status=status.HTTP_200_OK
    )
