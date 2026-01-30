from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser
from .pagination import StandardResultsSetPagination
from management.models import Title, Category, Genre, Review, Comment
from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer, UserSerializer,
                          ReviewSerializer, GetTokenSerializer, SignUpSerializer, CommentSerializer)
from .permissions import IsAdminOrReadOnly, IsAdminOrModeratorOrAuthor, IsAdmin


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'username'
    permission_classes = [IsAdmin,]

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    



class TitleViewSet(IsAdminOrReadOnly, viewsets.ModelViewSet):
    """
    Получение всех произведений, добавление нового произведения.
    /id/ Получение, удаление, изменение конкретного произведения
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = StandardResultsSetPagination


class CategoryViewSet(IsAdminOrReadOnly,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Получение, удаление, категорий произведений"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(IsAdminOrReadOnly,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Получение, удаление, жанров произведений"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class ReviewsViewSet(IsAdminOrModeratorOrAuthor, viewsets.ModelViewSet):
    """Получение, создание, изменение, удаление обзоров на произведений"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        new_queryset = Review.objects.filter(title=self.kwargs.get('title_pk'))
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_pk')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(IsAdminOrModeratorOrAuthor, viewsets.ModelViewSet):
    """Получение, создание, изменение, удаление комментариев на обзоры"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_pk'),
            title_id=self.kwargs.get('title_pk')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_pk')
        review = get_object_or_404(Title, id=review_id)
        serializer.save(author=self.request.user, review=review)