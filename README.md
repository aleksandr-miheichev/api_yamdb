# ArtReview Hub

## Содержание

- [Описание проекта](#Описание-проекта)
- [Технологический стек](#Технологический-стек)
- [Как развернуть проект](#как-развернуть-проект)
- [Шаблон наполнения файла .env](#шаблон-наполнения-файла-env)
- [Запуск приложения](#запуск-приложения)
- [Примеры работы с проектом](#Примеры-работы-с-проектом)
- [Инструкции для накачки базы из CSV-файлов](#Инструкции-для-накачки-базы-из-CSV-файлов)
- [Над проектом работали](#Над-проектом-работали)

---

### Описание проекта:

Проект собирает отзывы пользователей о различных произведениях искусства. Он
классифицирует эти произведения по различным типам, таким как "Книги", "Фильмы"
и "Музыка". Платформа не хранит сами произведения, она предназначена
исключительно для сбора отзывов. Пользователи могут оставлять текстовые отзывы
и оценивать произведения по шкале от одного до десяти. Каждый пользователь
может оставить только один отзыв на каждое произведение. Только авторизованные
пользователи могут оставлять отзывы, комментарии и оценки. Произведения могут
быть связаны с жанрами, и администраторы имеют исключительные права на
добавление произведений, категорий и жанров.

#### Роли пользователей и права доступа

- **Аноним**: может просматривать описания работ, читать отзывы и комментарии.
- **Аутентифицированный пользователь (user)**: наследует все права Anonymous,
  может размещать обзоры, оценивать работы и комментировать обзоры. Он также
  может редактировать или удалять свои отзывы, комментарии и оценки.
- **Модератор (moderator)**: наследует все права Пользователя плюс возможность
  редактировать или удалять любые отзывы и комментарии.
- **Администратор (admin)**: полные права на управление содержимым проекта,
  включая создание и удаление произведений, категорий и жанров. Он также может
  назначать роли пользователям.
- **Суперюзер Django (Django Superuser)**: всегда имеет права
  администратора, независимо от установленной роли пользователя.

#### Регистрация пользователей

Пользователи могут самостоятельно зарегистрироваться, отправив POST-запрос с
указанием электронной почты и имени пользователя. На электронную почту
высылается код подтверждения, который, будучи подтвержденным, предоставляет
пользователю JWT-токен. После регистрации пользователь может заполнить данные
своего профиля.

#### Управление данными

При удалении пользователя удаляются также все его отзывы и комментарии. При
удалении произведения удаляются все связанные с ним отзывы и комментарии, но
удаление категории или жанра не приводит к удалению связанных с ними
произведений. База данных может быть заполнена данными из предоставленных
csv-файлов, которые можно импортировать с помощью собственной команды
управления на Django.

---

### Технологический стек:

- [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
- [![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
- [![DjangoRestFramework](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
- [![Simple JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [Django Filter](https://django-filter.readthedocs.io/en/main/)

---

### Как развернуть проект:

Клонировать репозиторий и перейти в него в терминале используя команду

```bash
cd
```

```bash
git clone git@github.com:aleksandr-miheichev/review_ratings_platform.git
```

Создать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

---

### Шаблон наполнения файла .env:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=xxyyzz
DB_HOST=db
DB_PORT=5432
```

---

### Запуск приложения:

Чтобы запустить модуль, необходимо в терминале перейти в папку `api_yamdb`:

```bash
cd .\api_yamdb\
```

Далее необходимо применить миграции:

```bash
python manage.py migrate
```

После этого осуществить запуск приложения:

```bash
python manage.py runserver
```

Далее отрыть сайт с проектом перейдя по ссылке:

http://127.0.0.1:8000/

---

### Примеры работы с проектом:

Удобную веб-страницу со справочным меню, документацией для эндпоинтов и
разрешённых методов, с примерами запросов, ответов и кода Вы сможете посмотреть
по адресу:

[http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

### Инструкции для накачки базы из CSV-файлов:

Для загрузки данных, получаемых вместе с проектом, из файлов csv в базу данных
через Django ORM была написана собственная management-команда.

Увидеть её описание Вы сможете, открыв папку:

```bash
api_yamdb/api_yamdb
```

В терминале и далее введя команду:

```bash
python manage.py data_loading -h
```

Для выполнения процедуры загрузки в базу данных необходимо выполнить:

```bash
python manage.py data_loading
```

В случае успешного выполнения данной процедуры будет выведено сообщение в
терминал:

```bash
Database successfully loaded into models!
```

При отсутствии csv файла с данными или его неправильного наименования будет
выведена ошибка:

```bash
Sorry, the file "<название_файла>" does not exist.
```

При необходимости внести корректировки в данную management-команду Вы сможете
найдя её исполняющий файл в папке:

```bash
api_yamdb/api_yamdb/reviews/management/commands/data_loading.py
```

---

### Над проектом работали:

- [Михеичев Александр](https://github.com/aleksandr-miheichev)
- [Назаров Константин](https://github.com/K1N88)
- [Тищенко Николай](https://github.com/NikolayTishenko)
