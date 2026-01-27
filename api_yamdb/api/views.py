from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from .models import Title, Category, Genre
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer


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
