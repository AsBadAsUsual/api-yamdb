# YaMDB API

API для проекта **YaMDB** — базы данных произведений (фильмы, книги, музыка) с возможностью оставлять отзывы, ставить оценки и управлять контентом через роли пользователей.

**Репозиторий:** [https://github.com/AsBadAsUsual/api-yamdb](https://github.com/AsBadAsUsual/api-yamdb.git)

---

## Технологии

- Python 3.12  
- Django  
- Django REST Framework  
- PostgreSQL / SQLite  
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
В ответ придёт confirmation_code на email.

Получение токена
```POST /api/v1/auth/token/```

Параметры:
```
{
  "username": "user123",
  "confirmation_code": "123456"
}
```
В ответ JWT-токен.

Пользовательский профиль

```GET /api/v1/users/me/``` — получить данные
```PATCH /api/v1/users/me/``` — изменить данные

Пример cURL:

```curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/users/me/```

Управление пользователями (Администратор)
```
Метод	URL	Описание
GET	/api/v1/users/	Список всех пользователей
POST	/api/v1/users/	Создать пользователя
GET	/api/v1/users/<username>/	Получить пользователя
PATCH	/api/v1/users/<username>/	Изменить пользователя
DELETE	/api/v1/users/<username>/	Удалить пользователя
```

Пример запроса создания:

```OST /api/v1/users/```
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
```
Метод	URL	Описание
GET	/api/v1/titles/	Список всех произведений
POST	/api/v1/titles/	Создать произведение
GET	/api/v1/titles/<id>/	Получить произведение
PATCH	/api/v1/titles/<id>/	Изменить произведение
DELETE	/api/v1/titles/<id>/	Удалить произведение
```

Пример создания:

```POST /api/v1/titles/```
```
{
  "name": "Властелин колец",
  "year": 1954,
  "category": 1,
  "genre": [1, 2]
}
```

Reviews (Отзывы)
```
Метод	URL	Описание
GET	/api/v1/titles/<title_id>/reviews/	Список отзывов по произведению
POST	/api/v1/titles/<title_id>/reviews/	Создать отзыв
GET	/api/v1/titles/<title_id>/reviews/<review_id>/	Получить отзыв
PATCH	/api/v1/titles/<title_id>/reviews/<review_id>/	Изменить отзыв
DELETE	/api/v1/titles/<title_id>/reviews/<review_id>/	Удалить отзыв
```

Пример создания:

```POST /api/v1/titles/1/reviews/```
```
{
  "text": "Отличная книга!",
  "score": 10
}
```

Comments (Комментарии)
```
Метод	URL	Описание
GET	/api/v1/titles/<title_id>/reviews/<review_id>/comments/	Список комментариев к отзыву
POST	/api/v1/titles/<title_id>/reviews/<review_id>/comments/	Создать комментарий
GET	/api/v1/titles/<title_id>/reviews/<review_id>/comments/<comment_id>/	Получить комментарий
PATCH	/api/v1/titles/<title_id>/reviews/<review_id>/comments/<comment_id>/	Изменить комментарий
DELETE	/api/v1/titles/<title_id>/reviews/<review_id>/comments/<comment_id>/	Удалить комментарий
```

Пример:

```POST /api/v1/titles/1/reviews/1/comments/```
```
{
  "text": "Согласен с автором!"
}
```

Categories (Категории) и Genres (Жанры)
```
Метод	URL	Описание
GET	/api/v1/categories/	Список категорий
POST	/api/v1/categories/	Создать категорию (админ)
DELETE	/api/v1/categories/<slug>/	Удалить категорию (админ)
GET	/api/v1/genres/	Список жанров
POST	/api/v1/genres/	Создать жанр (админ)
DELETE	/api/v1/genres/<slug>/	Удалить жанр (админ)
```

Пример:
```POST /api/v1/genres/```
```
{
  "name": "Фэнтези",
  "slug": "fantasy"
}
```

## Роли пользователей
Аноним (Anonymous) — просмотр произведений и отзывов

Аутентифицированный пользователь — публикация отзывов, оценка произведений, редактирование своих данных

Модератор — редактирование/удаление любых отзывов и комментариев

Администратор — полный доступ к проекту, управление пользователями, категориями и жанрами

Суперпользователь Django — всегда администратор

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

# Над проектом работали: Селиванов Александр, Карпухин Тихон, Пономарёв Александр