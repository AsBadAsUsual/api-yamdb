import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

class Command(BaseCommand):
    """Импорт данных из CSV файлов в базу данных"""

    def handle(self, *args, **options):
        data_map = {
            self.import_users: 'users.csv',
            self.import_categories: 'category.csv',
            self.import_genres: 'genre.csv',
            self.import_titles: 'titles.csv',
            self.import_genre_titles: 'genre_title.csv',
            self.import_reviews: 'review.csv',
            self.import_comments: 'comments.csv',
        }

        for func, filename in data_map.items():
            path = os.path.join(settings.BASE_DIR, 'static', 'data', filename)
            if os.path.exists(path):
                func(path)
            else:
                self.stdout.write(
                    self.style.WARNING(f"Файл {filename} не найден."))

        self.stdout.write(self.style.SUCCESS("--- ИМПОРТ ЗАВЕРШЕН ---"))

    def import_users(self, path):
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            objs = [User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                role=row["role"]
            ) for row in reader]
            User.objects.bulk_create(objs, ignore_conflicts=True)
        self.stdout.write("Пользователи загружены")

    def import_categories(self, path):
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            objs = [Category(
                id=row.get("id"),
                name=row["name"],
                slug=row["slug"]
            ) for row in reader]
            Category.objects.bulk_create(objs, ignore_conflicts=True)
        self.stdout.write("Категории загружены")

    def import_genres(self, path):
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            objs = [Genre(
                id=row.get("id"),
                name=row["name"],
                slug=row["slug"]
            ) for row in reader]
            Genre.objects.bulk_create(objs, ignore_conflicts=True)
        self.stdout.write("Жанры загружены")

    def import_titles(self, path):
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            objs = [
                Title(
                    id=row["id"],
                    name=row["name"],
                    year=row["year"],
                    category_id=row["category"]
                ) for row in reader
            ]
            Title.objects.bulk_create(objs, ignore_conflicts=True)
        self.stdout.write("Произведения загружены")

    def import_genre_titles(self, path):
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            through_model = Title.genre.through
            objs = [
                through_model(
                    title_id=row["title_id"],
                    genre_id=row["genre_id"])
                for row in reader
            ]
            through_model.objects.bulk_create(objs, ignore_conflicts=True)
        self.stdout.write("Связи жанров и произведений загружены")

    def import_reviews(self, path):
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            objs = [
                Review(
                    id=row["id"],
                    text=row["text"],
                    author_id=row["author"],
                    score=row["score"],
                    pub_date=row["pub_date"],
                    title_id=row["title_id"],
                ) for row in reader
            ]
            Review.objects.bulk_create(objs, ignore_conflicts=True)
        self.stdout.write("Отзывы загружены")

    def import_comments(self, path):
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            objs = [
                Comment(
                    id=row["id"],
                    review_id=row["review_id"],
                    text=row["text"],
                    author_id=row["author"],
                    pub_date=row["pub_date"],
                ) for row in reader
            ]
            Comment.objects.bulk_create(objs, ignore_conflicts=True)
        self.stdout.write("Комментарии загружены")