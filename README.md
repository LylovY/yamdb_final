# Api для проекта Yamdb

![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white)
![api_yamdb workflow](https://github.com/LylovY/
yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


Yamdb - проект, собирающий отзывы пользователей на произведения. Сами произведения в Yamdb не хранятся. Yamdb поддерживает следующий функционал:

- Публикование отзывов
- Комментирование отзывов
- Регистрация пользователей
- Изменение пользователями своих профилей, отзывов и комментариев

## Пользовательские роли

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django обладает всеми правами администратора

Api предоставляет полноценный доступ к функционалу Yatube

## шаблон наполнения .env файла директории /infra

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql

DB_NAME=postgres # имя базы данных

POSTGRES_USER=# логин для подключения к базе данных

POSTGRES_PASSWORD= # пароль для подключения к БД (установите свой)

DB_HOST=db # название сервиса (контейнера)

DB_PORT=5432 # порт для подключения к БД


## Установка

Клонировать репозиторий:

```
git clone git@github.com:LylovY/infra_sp2.git
```

Перейти в директорию c файлом docker-compose

```
cd infra_sp2/infra
```
Запустите docker-compose командой:

```
docker-compose up -d
```

Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создать superuser:

```
docker-compose exec web python manage.py createsuperuser
```
Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```
Посмотреть ID контейнера web:

```
docker ps
```

Скопировать файл fixtures,json в контейнер:

```
docker cp fixtures.json ID-container:/app/fixtures.json
```
Загрузить данные в БД:

```
docker-compose exec web python3 manage.py loaddata fixtures.json
```



## Примеры

http://localhost/api/v1/users/

GET
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```

POST
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
http://localhost/api/v1/categories/

GET
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

POST
```
{
  "name": "string",
  "slug": "string"
}
```

http://localhost/api/v1/genres/


GET
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

POST
```
{
  "name": "string",
  "slug": "string"
}
```

http://localhost/api/v1/titles/{titles_id}/

PATCH
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

http://localhost/api/v1/titles/{title_id}/reviews/

GET
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2022-08-14T14:15:22Z"
      }
    ]
  }
]
```

POST
```
{
  "text": "string",
  "score": 1
}
```

http://localhost/api/v1/titles/{title_id}/reviews/{review_id}/comments/

GET
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2022-08-14T14:15:22Z"
      }
    ]
  }
]
```

POST
```
{
  "text": "string"
}
```
