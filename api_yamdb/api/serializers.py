import datetime as dt
from rest_framework import serializers

from .models import Title, Category, Genre
from users.models import CustomUser


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ("id", "name", "year", "category", "genre", "description")

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения будущего!')
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("name", "slug")
