import datetime as dt
import re

from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from rest_framework import serializers
from reviews.constants import (
    EMAIL_MAX_LENGTH,
    FORBIDDEN_USERNAME,
    USERNAME_MAX_LENGTH,
    USERNAME_REGEX,
)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UsernameValidationMixin:
    def validate_username(self, value):
        if not re.match(USERNAME_REGEX, value):
            raise serializers.ValidationError(
                "Недопустимые символы в username"
            )
        if len(value) > USERNAME_MAX_LENGTH:
            raise serializers.ValidationError("Username слишком длинный")
        if value == FORBIDDEN_USERNAME:
            raise serializers.ValidationError(
                f"Имя {FORBIDDEN_USERNAME} запрещено"
            )
        return value


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class UserSerializer(UsernameValidationMixin, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and not (
            request.user.is_authenticated and request.user.is_admin
        ):
            fields["role"].read_only = True
        return fields


class SignUpSerializer(UsernameValidationMixin, serializers.Serializer):

    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH, required=True
    )

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")

        user_and_email = User.objects.filter(
            email=email, username=username
        ).first()

        if user_and_email:
            return data

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": ["Пользователь с таким email уже зарегистрирован."]}
            )

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": ["Этот username уже занят."]}
            )

        return data

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data["username"]

        user, created = User.objects.get_or_create(
            email=email, username=username
        )
        user.confirmation_code = default_token_generator.make_token(user)
        return user


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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def get_rating(self, obj):
        total_rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        if total_rating is not None:
            return round(total_rating, 1)
        return None


class TitleWriteSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError(
                "Нельзя добавлять произведения будущего!"
            )
        return value

    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError(
                "Произведение должно иметь хотя бы один жанр."
            )
        return value

    def to_representation(self, instance):
        serializer = TitleReadSerializer(instance)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

    def validate(self, data):
        request = self.context.get("request")
        if request.method != "POST":
            return data

        user = request.user
        title_id = self.context["view"].kwargs.get("title_pk")
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError(
                "Вы уже оставили отзыв на это произведение."
            )
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
