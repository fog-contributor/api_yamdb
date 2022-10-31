# YaMDb API

## Описание
Учебный командный проект **YaMDb** собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». К отзыву можно оставить комментарий.


## Как развернуть проект на локальной машине:


* Склонировать репозиторий:
```
git clone https://github.com/fog-contributor/api_yamdb.git
```

```
cd api_yamdb
```

* Cоздать виртуальное окружение:
```
python3 -m venv venv
```
* Активировать виртуальное окружение:
```
source env/bin/activate
```
* Обновить пакетный менеджер: 
```
python -m pip install --upgrade pip
```

* Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

* Выполнить миграции:

```
python manage.py migrate
```

* Запустить проект:

```
python manage.py runserver
```
* Заполнить БД тестовыми данными из csv-таблиц.
```
python3 manage.py add_csv
```
## Примеры запросов:
