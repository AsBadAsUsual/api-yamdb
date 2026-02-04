from django.conf import settings
from django.db import models

from reviews.constants import NAME_MAX_LENGTH, SYMBOLS_FOR_TEXT_FIELD
from reviews.validators import validate_score, validate_year


class CategoryGenreBase(models.Model):
    name = models.CharField("Название", max_length=NAME_MAX_LENGTH)
    slug = models.SlugField("Слаг", unique=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name


class CommentReviewBase(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    text = models.TextField("Текс отзыва")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:SYMBOLS_FOR_TEXT_FIELD]


class Category(CategoryGenreBase):

    class Meta(CategoryGenreBase.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(CategoryGenreBase):

    class Meta(CategoryGenreBase.Meta):
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.CharField("Название", max_length=NAME_MAX_LENGTH)
    year = models.SmallIntegerField(
        validators=[validate_year],
        verbose_name="Год выпуска",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория произведения",
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр произведения",
    )
    description = models.TextField("Описание произведения")

    class Meta:
        ordering = ["name"]
        default_related_name = "titles"
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(CommentReviewBase):

    score = models.PositiveSmallIntegerField(
        validators=[validate_score],
        verbose_name="Оценка",
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="Публикация"
    )

    class Meta(CommentReviewBase.Meta):
        default_related_name = "reviews"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(CommentReviewBase):

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name="Отзыв"
    )

    class Meta(CommentReviewBase.Meta):
        default_related_name = "comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
