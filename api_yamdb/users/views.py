from smtplib import SMTPResponseException

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdminOrSuperUser
from .serializers import (RegistrationSerializer, TokenSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminOrSuperUser,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('role'):
            serializer.validated_data['role'] = request.user.role
        serializer.save()
        return Response(serializer.data)


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
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(username=username, email=email)
    user.save()

    token = default_token_generator.make_token(user)
    try:
        send_mail(
            'Token',
            f'{token}',
            'Cuencaldd@ya.ru',
            [email],
            fail_silently=False,
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except SMTPResponseException:
        user.delete()
        return Response(
            data={
                'error': 'Ошибка отправки кода подтверждения!',
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            data={'error': 'Неподходящий токен'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    token = RefreshToken.for_user(user)
    return Response(
        data={'access': str(token.token)}, status=status.HTTP_200_OK
    )
