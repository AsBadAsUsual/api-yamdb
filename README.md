# YaMDB API

API для проекта **YaMDB** — базы данных произведений (фильмы, книги, музыка) с возможностью оставлять отзывы, ставить оценки и управлять контентом через роли пользователей.

**Репозиторий:** [https://github.com/AsBadAsUsual/api-yamdb](https://github.com/AsBadAsUsual/api-yamdb.git)

---

## Технологии

- Python 3.12  
- Django  
- Django REST Framework  
- SQLite  
- JWT для авторизации  

---

## Установка и запуск

1. Клонируем репозиторий:  
```
git clone https://github.com/AsBadAsUsual/api-yamdb.git
cd api-yamdb
```

2. Создаём виртуальное окружение и активируем:
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Устанавливаем зависимости:
```
pip install -r requirements.txt
```
4. Настраиваем .env или переменные окружения (пример):
```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
```
5. Выполняем миграции:
```
python manage.py migrate
```
6. Создаём суперпользователя (админ):
```
python manage.py createsuperuser
```
7. Запускаем сервер:
```
python manage.py runserver
```
8. Наполняем базы данных данными из csv файлов
```
python manage.py import_csv
```
## Использование API
Регистрация пользователя

```POST /api/v1/auth/signup/```

Параметры:

```
{
  "email": "user@example.com",
  "username": "user123"
}
```

Ответ(200 OK)
```
{
  "username": "alex",
  "email": "alex@example.com"
}
```
После этого на имейл приходит код подтверждения.

Получение токена
```POST /api/v1/auth/token/```

Параметры:
```
{
  "username": "user123",
  "confirmation_code": "123456"
}
```
Ответ:
```
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Пользовательский профиль

```GET /api/v1/users/me/``` — получить данные

```PATCH /api/v1/users/me/``` — изменить данные

Пример cURL:

```curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/users/me/```

Управление пользователями (Администратор)

| Метод | URL | Описание | Доступ |
|------|-----|----------|--------|
| GET | /api/v1/users/ | Список пользователей | admin |
| POST | /api/v1/users/ | Создание пользователя | admin |
| GET | /api/v1/users/{username}/ | Получение пользователя | admin |
| PATCH | /api/v1/users/{username}/ | Изменение пользователя | admin |
| DELETE | /api/v1/users/{username}/ | Удаление пользователя | admin |


Пример запроса создания:

```POST /api/v1/users/```
```
{
  "username": "new_user",
  "email": "new@example.com",
  "role": "user",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "bio": "Описание"
}
```

Titles (Произведения)

| Метод | URL | Описание | Доступ |
|------|-----|----------|--------|
| GET | /api/v1/titles/ | Список произведений | Любой |
| POST | /api/v1/titles/ | Создание произведения | admin |
| GET | /api/v1/titles/{id}/ | Получение произведения | Любой |
| PATCH | /api/v1/titles/{id}/ | Редактирование произведения | admin |
| DELETE | /api/v1/titles/{id}/ | Удаление произведения | admin |


Пример создания:

```POST /api/v1/titles/```
```
{
  "name": "1984",
  "year": 1949,
  "description": "Антиутопия",
  "genre": ["drama"],
  "category": "books"
}
```
Ответ:
```
{
  "id": 2,
  "name": "1984",
  "year": 1949,
  "rating": null,
  "description": "Антиутопия",
  "genre": [
    {
      "name": "Драма",
      "slug": "drama"
    }
  ],
  "category": {
    "name": "Книги",
    "slug": "books"
  }
}
```

Reviews (Отзывы)

| Метод | URL | Описание | Доступ |
|------|-----|----------|--------|
| GET | /api/v1/titles/{title_id}/reviews/ | Список отзывов | Любой |
| POST | /api/v1/titles/{title_id}/reviews/ | Создание отзыва | user |
| GET | /api/v1/titles/{title_id}/reviews/{id}/ | Получение отзыва | Любой |
| PATCH | /api/v1/titles/{title_id}/reviews/{id}/ | Редактирование отзыва | Автор / moderator / admin |
| DELETE | /api/v1/titles/{title_id}/reviews/{id}/ | Удаление отзыва | Автор / moderator / admin |


Пример создания:

```POST /api/v1/titles/1/reviews/```
```
{
  "text": "Отличный фильм!",
  "score": 10
}
```
Ответ:
```
{
  "id": 1,
  "text": "Отличный фильм!",
  "author": "alex",
  "score": 10,
  "pub_date": "2026-02-02T10:15:30Z"
}
```

Comments (Комментарии)

| Метод | URL | Описание | Доступ |
|------|-----|----------|--------|
| GET | /api/v1/titles/{title_id}/reviews/{review_id}/comments/ | Список комментариев | Любой |
| POST | /api/v1/titles/{title_id}/reviews/{review_id}/comments/ | Создание комментария | user |
| PATCH | /api/v1/titles/{title_id}/reviews/{review_id}/comments/{id}/ | Редактирование комментария | Автор / moderator / admin |
| DELETE | /api/v1/titles/{title_id}/reviews/{review_id}/comments/{id}/ | Удаление комментария | Автор / moderator / admin |


Пример:

```POST /api/v1/titles/1/reviews/1/comments/```
```
{
  "text": "Полностью согласен"
}
```
Ответ:
```
{
  "id": 1,
  "text": "Полностью согласен",
  "author": "mike",
  "pub_date": "2026-02-02T10:20:10Z"
}
```

Categories (Категории) и Genres (Жанры)

| Метод | URL | Описание | Доступ |
|------|-----|----------|--------|
| GET | /api/v1/categories/ | Список категорий | Любой |
| POST | /api/v1/categories/ | Создание категории | admin |
| DELETE | /api/v1/categories/{slug}/ | Удаление категории | admin |
| GET | /api/v1/genres/ | Список жанров | Любой |
| POST | /api/v1/genres/ | Создание жанра | admin |
| DELETE | /api/v1/genres/{slug}/ | Удаление жанра | admin |


Пример:
```GET /api/v1/genres/```

Ответ:
```
[
  {
    "name": "Драма",
    "slug": "drama"
  },
  {
    "name": "Комедия",
    "slug": "comedy"
  }
]
```

## Роли пользователей
**Аноним** (Anonymous) — просмотр произведений и отзывов

**Аутентифицированный пользователь** — публикация отзывов, оценка произведений, редактирование своих данных

**Модератор** — редактирование/удаление любых отзывов и комментариев

**Администратор** — полный доступ к проекту, управление пользователями, категориями и жанрами

**Суперпользователь Django** — всегда администратор

## Структура проекта
```
api-yamdb/
├── api/
│   ├── serializers.py
│   ├── views.py
├── users/
│   ├── models.py
│   ├── serializers.py
├── manage.py
├── requirements.txt
├── .env
```

###### Над проектом работали: Селиванов Александр, Карпухин Тихон, Пономарёв Александр