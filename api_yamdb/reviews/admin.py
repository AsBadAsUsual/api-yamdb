from django.contrib import admin
from .models import (Category, Comment, Genre,
                     Review, Title)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'text',
        'pub_date',
        'review'
    )
    ordering = ('-pub_date',)
    search_fields = ('author', 'review', 'pub_date')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'text',
        'score',
        'pub_date',
        'title',
    )
    ordering = ('-pub_date',)
    search_fields = (
        'author',
        'score',
        'pub_date',
        'title',
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'category',
        'get_genres',
        'description',
    )

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])

    get_genres.short_description = 'Жанры'
    ordering = ('name',)
    search_fields = ('name', 'year')
