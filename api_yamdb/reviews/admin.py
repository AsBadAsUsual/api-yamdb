from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "text", "pub_date", "review")
    ordering = ("-pub_date",)
    search_fields = ("author__username", "review__text", "pub_date")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "text",
        "score",
        "pub_date",
        "title",
    )
    ordering = ("-pub_date",)
    search_fields = (
        "author__username",
        "score",
        "pub_date",
        "title__text",
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "year",
        "category",
        "get_genres",
        "description",
    )
    ordering = ("name",)
    search_fields = ("name", "year")

    @admin.display(description="Жанры")
    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
