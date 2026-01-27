from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Title, Category, Genre
from .serializers import TitlesSerializer, TitleSerializer, CategorySerializer, GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """Получение всех произведений, добавление нового произведения"""
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [AllowAny,]

class TitleViewSet(viewsets.ModelViewSet):
    """Получение, удаление, изменение конкретного произведения"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [AllowAny,]

class CategoryViewSet(viewsets.ModelViewSet):
    """Получение, удаление, изменение категорий произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny,]

class GenreViewSet(viewsets.ModelViewSet):
    """Получение, удаление, изменение жанров произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny,]