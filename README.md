# YaMDb

Учебный REST API для каталога произведений, оценок, отзывов и комментариев. Произведения группируются по категориям и жанрам, рейтинг вычисляется из оценок. В API есть регистрация по коду подтверждения и роли пользователя, модератора и администратора.

## Стек

Python, Django 3.2, Django REST Framework 3.12, Simple JWT, django-filter и SQLite. Версии зависимостей перечислены в `requirements.txt`. Текущий набор тестов проверен в локальном окружении с Python 3.12.6; стек учебный и давно не обновлялся.

## Запуск

Из корня репозитория создайте виртуальное окружение, активируйте его и установите зависимости:

```sh
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Задайте `SECRET_KEY` в окружении. Пример значений есть в `.env.example`; файл не загружается автоматически. Для локального PowerShell:

```powershell
$env:SECRET_KEY = 'replace-with-a-long-random-secret-key'
$env:DEBUG = 'True'
```

На Linux/macOS используйте `export SECRET_KEY=...` и `export DEBUG=True`. В `ALLOWED_HOSTS` можно указать хосты через запятую; по умолчанию разрешены `localhost` и `127.0.0.1`. Затем:

```sh
cd api_yamdb
python manage.py migrate
python manage.py runserver
```

API доступен по `http://127.0.0.1:8000/api/v1/`, локальная документация — по `/redoc/`. Регистрация: `POST /api/v1/auth/signup/` с `email` и `username`; код приходит в файловый почтовый backend `api_yamdb/sent_emails/`. Затем `POST /api/v1/auth/token/` с `username` и `confirmation_code` выдаёт JWT access token. Для защищённых запросов используйте заголовок `Authorization: Bearer <token>`.

После миграций можно загрузить демонстрационные CSV: `python manage.py import_csv`. Команда записывает данные в локальную SQLite-базу, поэтому запускайте её только для новой или предназначенной для демонстрации базы.

## Проверка

Из корня репозитория с активным окружением и заданным `SECRET_KEY`:

```sh
python -m pytest -q
cd api_yamdb
python manage.py check
```

Проект использует SQLite и файловую отправку писем для локальной разработки. Он не содержит настроенного продакшен-развёртывания.
