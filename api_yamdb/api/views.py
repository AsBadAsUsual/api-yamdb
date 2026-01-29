from rest_framework import viewsets, mixins
from django.core.mail import EmailMessage
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser
from .pagination import StandardResultsSetPagination
from .models import Title, Category, Genre, Review
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer, ReviewSerializer, GetTokenSerializer, SignUpSerializer


class APIGetToken(APIView):
    """
    Получение JWT-токена при использовании username и confirmation code.
    Доступно без токена.
    """
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = CustomUser.objects.get(username=data['username'])
        except CustomUser.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """
    Получить код подтверждения на переданный email. Права доступа: Доступно без
    токена. Поля email и username должны быть уникальными.
    """
    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Приветствую, {user.username}.'
            f'\nКод подтверждения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения для доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PermissionMixin:
    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [AllowAny()]
        return [AllowAny()]


class TitleViewSet(PermissionMixin, viewsets.ModelViewSet):
    """
    Получение всех произведений, добавление нового произведения.
    /id/ Получение, удаление, изменение конкретного произведения
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = StandardResultsSetPagination


class CategoryViewSet(PermissionMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Получение, удаление, категорий произведений"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(PermissionMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Получение, удаление, жанров произведений"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class ReviewsViewSet(PermissionMixin, viewsets.ModelViewSet):
    """Получение, создание, изменение, удаление обзоров на произведений"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
