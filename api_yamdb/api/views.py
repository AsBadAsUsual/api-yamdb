from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Title, Category, Genre
from .serializers import TitlesSerializer, TitleSerializer, CategorySerializer, GenreSerializer


class TitlesViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Получение всех произведений, добавление нового произведения"""
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [AllowAny,]

class TitleViewSet(viewsets.ModelViewSet):
    """Получение, удаление, изменение конкретного произведения"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [AllowAny,]

class CategoryViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Получение, удаление, изменение категорий произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny,]

class GenreViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Получение, удаление, изменение жанров произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny,]