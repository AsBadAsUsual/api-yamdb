import datetime as dt
import re
from rest_framework import serializers

from django.core.validators import RegexValidator

from reviews.models import Title, Category, Genre, Review, Comment
from users.models import CustomUser


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "confirmation_code"
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and not (request.user.is_authenticated and request.user.is_admin):
            fields['role'].read_only = True
        return fields

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'Недопустимые символы в username'
            )
        if len(value) > 150:
            raise serializers.ValidationError(
                'Username слишком длинный'
            )
        if value == 'me':
            raise serializers.ValidationError(
                'Имя "me" запрещено'
            )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("email", "username")

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'Недопустимые символы в username'
            )
        if len(value) > 150:
            raise serializers.ValidationError(
                'Username слишком длинный'
            )
        if value == 'me':
            raise serializers.ValidationError(
                'Имя "me" запрещено'
            )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ("id", "name", "year", "rating", "description", "genre", "category")


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError("Нельзя добавлять произведения будущего!")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username",
    read_only=True)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("author", "pub_date")

    def validate(self, data):
        request = self.context.get("request")
        if request.method != "POST":
            return data

        user = request.user
        if not user or user.is_anonymous:
            return data

        title_id = self.context["view"].kwargs.get("title_pk")
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError("Вы уже оставили отзыв на это произведение.")
        return data

class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("author", "pub_date")