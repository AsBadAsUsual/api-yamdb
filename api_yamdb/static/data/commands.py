import csv
import os
import sys

import django
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title

project_path = "C:/Users/Ti/Documents/Pyton/api-yamdb/api_yamdb/"
sys.path.append(project_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_yamdb.settings")
django.setup()


User = get_user_model()


class Command(BaseCommand):

    def category(self, *args, **options):
        with open(
            "C:/Users/Ti/Documents/Pyton/api-yamdb/"
            "api_yamdb/static/data/category.csv",
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            objs = [
                Category(name=row["name"], slug=row["slug"]) for row in reader
            ]
            Category.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))

    def genre(self, *args, **options):
        with open(
            "C:/Users/Ti/Documents/Pyton/api-yamdb/"
            "api_yamdb/static/data/genre.csv",
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            objs = [
                Genre(name=row["name"], slug=row["slug"]) for row in reader
            ]
            Genre.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))

    def titles(self, *args, **options):
        with open(
            "C:/Users/Ti/Documents/Pyton/api-yamdb/"
            "api_yamdb/static/data/titles.csv",
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            objs = [
                Title(
                    name=row["name"],
                    year=row["year"],
                    category_id=row["category"],
                )
                for row in reader
            ]
            Title.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))

    def genre_title(self):
        path = "C:/Users/Ti/Documents/Pyton/api-yamdb/"
        "api_yamdb/static/data/genre_title.csv"
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            through_model = Title.genre.through

            objs = [
                through_model(
                    title_id=row["title_id"], genre_id=row["genre_id"]
                )
                for row in reader
            ]
            through_model.objects.bulk_create(objs, ignore_conflicts=True)
        print("Связи жанров и произведений загружены")

    def review(self, *args, **options):
        with open(
            "C:/Users/Ti/Documents/Pyton/api-yamdb/"
            "api_yamdb/static/data/review.csv",
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            objs = [
                Review(
                    id=row["id"],
                    text=row["text"],
                    author_id=row["author"],
                    score=row["score"],
                    pub_date=row["pub_date"],
                    title_id=row["title_id"],
                )
                for row in reader
            ]
            Review.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))

    def comments(self, *args, **options):
        with open(
            "C:/Users/Ti/Documents/Pyton/api-yamdb/"
            "api_yamdb/static/data/comments.csv",
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            objs = [
                Comment(
                    id=row["id"],
                    review_id=row["review_id"],
                    text=row["text"],
                    author_id=row["author"],
                    pub_date=row["pub_date"],
                )
                for row in reader
            ]
            Comment.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))

    def users(self, *args, **options):
        with open(
            "C:/Users/Ti/Documents/Pyton/api-yamdb/"
            "api_yamdb/static/data/users.csv",
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            objs = [
                User(
                    id=row["id"],
                    username=row["username"],
                    email=row["email"],
                    role=row["role"],
                )
                for row in reader
            ]
            User.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))


if __name__ == "__main__":
    command = Command()
    command.users()
    command.category()
    command.genre()
    command.titles()
    command.review()
    command.comments()
