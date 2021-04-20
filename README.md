# API для системы опросов пользователей

<details>
  <summary>Требования</summary>

Функционал для администратора:

- авторизация;
- добавление/изменение/удаление опросов.
Атрибуты опроса: название, дата старта, дата окончания, описание.
После создания поле "дата старта" изменять нельзя;
- добавление/изменение/удаление вопросов в опросе.
Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов).

Функционал для пользователей:

- получение списка активных опросов;
- прохождение опроса: опросы можно проходить анонимно; в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов;
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID пользователя.

Использовать Django 2.2.10, Django REST Framework.
</details>

## Запуск

Поочерёдно выполнить команды

```
docker-compose up
docker-compose exec django ./manage.py migrate
docker-compose exec django ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'password')"
```

Сервис доступен по адресу http://127.0.0.1:8080

Получить токен авторизации
```
curl -X POST "http://localhost:8080/api-auth/login/" -d "username=admin&password=password"
```
В ответ будет дан ключ
`{"key":"a14ef6eb828792c2e9cbea4b40b7de5e718f4f23"}`.

Его надо использовать в заголовке запросов, требующих авторизации:

`-H "Authorization: Token a14ef6eb828792c2e9cbea4b40b7de5e718f4f23"`

## Управление опросами

### Создание опроса

__POST /polls/__

Запрос

```
curl -X POST -H "Authorization: Token a14ef6eb828792c2e9cbea4b40b7de5e718f4f23" -H "Content-Type: application/json" "http://localhost:8080/polls/" -d "@sample.json"
```

Ответ

```
{
  "id": 1,
  "url": "http://127.0.0.1:8080/polls/1",
  "questions": [
    {
      "id": 1,
      "answers": [],
      "text": "Вопрос с ответом текстом",
      "type": "text"
    },
    {
      "id": 2,
      "answers": [
        {
          "text": "Ответ 1"
        },
        {
          "text": "Ответ 2"
        },
        {
          "text": "Ответ 3"
        }
      ],
      "text": "Вопрос с одним вариантом ответа",
      "type": "single_choice"
    },
    {
      "id": 3,
      "answers": [
        {
          "text": "Ответ 1"
        },
        {
          "text": "Ответ 2"
        },
        {
          "text": "Ответ 3"
        }
      ],
      "text": "Вопрос с несколькими вариантами ответа",
      "type": "multi_choice"
    }
  ],
  "title": "Опрос 1",
  "start_time": "2021-04-17T14:42:45+03:00",
  "end_time": "2021-04-30T14:43:45+03:00",
  "description": "Описание опроса"
}
```

### Изменение данных

__PUT /polls/<poll_id>/__

Изменить данные можно PUT-запросом на URL опроса (указан в ответе).
Можно изменить список вопросов/ответов, они добавятся/изменятся/удалятся.

Время старта опроса изменить нельзя.

### Удаление опроса

__DELETE /polls/<poll_id>/__


## Участие в опросе

Активные опросы находятся по пути `/active-polls/` и доступны без авторизации.

```
curl -X GET "http://localhost:8080/active-polls/"
```

### Отправка результата

__POST /results/__

На входе ожидается JSON такого формата:

```
{
  "user": 1,
  "poll_id": 1,
  "answers": [
    {
      "question_id": 1,
      "answer": "Ответ"
    },
    {
      "question_id": 2,
      "answer": "Ответ 1"
    },
    {
      "question_id": 3,
      "answer": "Ответ 2, Ответ 3"
    }
  ]
}
```

Запрос

```
curl -X POST -H "Content-Type: application/json" "http://localhost:8080/results/" -d '{"user":1,"poll_id":1,"answers":[{"question_id":1,"answer":"Ответ"},{"question_id":2,"answer":"Ответ 1"},{"question_id":3,"answer":"Ответ 2, Ответ 3"}]}'
```

### Получение результата по ID пользователя

__GET /results/?user_id=<user_id>__

Запрос

```
curl -X GET -H "Authorization: Token a14ef6eb828792c2e9cbea4b40b7de5e718f4f23" "http://localhost:8080/results/?user_id=1"
```

Ответ

```
{
  "answers": [
    {
      "question": "Вопрос с ответом текстом",
      "question_id": 1,
      "answer": "Ответ"
    },
    {
      "question": "Вопрос с одним вариантом ответа",
      "question_id": 2,
      "answer": "Ответ 1"
    },
    {
      "question": "Вопрос с несколькими вариантами ответа",
      "question_id": 3,
      "answer": "Ответ 2, Ответ 3"
    }
  ],
  "poll": "http://localhost:8080/polls/1",
  "poll_id": 1,
  "user": 1
}
```
