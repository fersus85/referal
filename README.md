# API Referal FastAPI app

## Technology Stack and Features
- FastAPI для Python бекэнд API
- SQLAlchemy в качестве ORM
- Pydantic для валидации данных
- PostgreSQL в качестве базы данных
- Redis in-memory база данных для кеширования
- Docker compose для развертывания приложения
- Безопасное хеширование паролей по умолчанию
- JWT token аутентификация (Oauth2.0)
- Отправка пользователю Email с реферальным кодом
- Аутентифицированный пользователь имеет возможность создать или удалить свой реферальный код
  - Одновременно может быть активен только 1 код
  - При создании кода задаётся его срок годности
- Возможность регистрации по реферальному коду в качестве реферала
- Получение информации о рефералах по id реферера
- UI документация (Swagger/ReDoc).
- Кеширование реферальных кодов с использованием Redis

### Configure

Вам необходимо изменить файл `.env` чтобф настроить вашу конфигурацию.

Как минимум, нужно переопределить следующие переменные:

- `SECRET_KEY`
- `FIRST_SUPERUSER_PASSWORD`
- `POSTGRES_PASSWORD`

## How To Use It

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/fersus85/referal.git
    ```
2. Перейдите в директорию проекта:
    ```bash
    cd referal
    ```
3. Запустите docker-compose:
  ```bash
    docker compose up -d
  ```
