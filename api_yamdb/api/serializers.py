from rest_framework import serializers

from .models import Title, Category, Genre


class TitlesSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'category', 'genre', 'description')
        read_only_fields = ('id',)

class TitleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'category', 'genre', 'description')
        read_only_fields = ('id',)

class CategorySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'category', 'genre', 'description')
        read_only_fields = ('id',)

class GenreSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Genre
        fields = ('id', 'name', 'category', 'genre', 'description')
        read_only_fields = ('id',)