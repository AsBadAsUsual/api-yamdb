import datetime as dt
from rest_framework import serializers

from .models import Title, Category, Genre, Review


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ("id", "name", "year","category", "genre", "description")

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError('Нельзя добавлять произведения будущего!')
        return value

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name", "slug")

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("name", "slug")

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
    read_only=True)

    class Meta:
        model = Review
        fields = ("author", "text", "score", "pub_date", "title")
        read_only_fields = ('author', 'pub_date')