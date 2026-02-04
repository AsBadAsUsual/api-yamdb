from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import TitleFilter
from api.pagination import StandardResultsSetPagination
from api.permissions import (IsAdmin, IsAdminOrModeratorOrAuthor,
                             IsAdminOrReadOnly)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleWriteSerializer,
    UserSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class APIGetToken(APIView):
    """
    Получение JWT-токена при использовании username и confirmation code.

    Права доступа: Доступно без токена.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = AccessToken.for_user(user)

        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK,
        )


class APISignup(APIView):
    """
    Получить код подтверждения на переданный email.

    Права доступа: Доступно без токена. Использовать имя 'me' в качестве
    username запрещено. Поля email и username должны быть уникальными.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
        )
        confirmation_code = default_token_generator.make_token(user)
        email_body = (
            f"Приветствую, {user.username}."
            f"\nКод подтверждения для доступа к API: {confirmation_code}"
        )

        send_mail(
            subject="Код подтверждения для API Yamdb",
            message=email_body,
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "username"
    permission_classes = [
        IsAdmin,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email"]

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получение всех произведений, добавление нового произведения.

    /id/ Получение, удаление, изменение конкретного произведения
    """

    queryset = Title.objects.annotate(rating=Avg("reviews__score")).order_by(
        "name"
    )

    serializer_class = TitleWriteSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = StandardResultsSetPagination
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Базовый ViewSet для категорий и жанров."""

    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(ListCreateDestroyViewSet):
    """Получение, удаление, категорий произведений"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """Получение, удаление, жанров произведений"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BaseCommentReviewViewSet(viewsets.ModelViewSet):
    """Базовый класс для отзывов и комментариев."""

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    pagination_class = StandardResultsSetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrModeratorOrAuthor,
    )


class ReviewsViewSet(BaseCommentReviewViewSet):
    """Получение, создание, изменение, удаление обзоров на произведений"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_pk"))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentsViewSet(BaseCommentReviewViewSet):
    """Получение, создание, изменение, удаление комментариев на обзоры"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get("review_pk"),
            title_id=self.kwargs.get("title_pk"),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
