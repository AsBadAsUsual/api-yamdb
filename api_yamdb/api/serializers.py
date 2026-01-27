from rest_framework import serializers

from .models import Title, Category, Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ("id", "name", "year","category", "genre", "description")

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name", "slug")

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("name", "slug")