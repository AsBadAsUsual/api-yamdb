import datetime as dt
from rest_framework import serializers

from management.models import Title, Category, Genre, Review, Comment
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


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'lust_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("email", "username")


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "category", "genre", "description")

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError("Нельзя добавлять произведения будущего!")
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
    author = serializers.SlugRelatedField(slug_field="username",
    read_only=True)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("author", "pub_date")

    def validate(self, data):
        request = self.context.get("request")
        if request and request.method == "POST":
            user = request.user
            title_id = self.context["view"].kwargs.get("title_pk")
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError("Вы уже оставили отзыв на это произведение.")
        return data

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("author", "pub_date")