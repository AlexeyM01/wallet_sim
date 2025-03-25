# wallet sumilation

## Назначение проекта

Этот проект представляет собой RESTful API для управления кошельками и операциями с ними. Он позволяет пользователям выполнять такие действия, как внесение и снятие средств с кошелька, а также получение текущего баланса. Приложение разработано с учетом конкурентной среды, что обеспечивает корректную обработку параллельных запросов на изменение баланса.

## Системные требования

- **Язык программирования**: Python 3.9 или выше
- **База данных**: PostgreSQL 13 или выше
- **Docker**: версия 20.10.0 или выше (для контейнеризации приложения)
- **Docker Compose**: версия 1.27.0 или выше

### Системные зависимости

- **Python библиотеки**:
  - fastapi
  - uvicorn
  - sqlalchemy
  - asyncpg
  - pydantic
  - python-dotenv
  - alembic
  - pytest

## Шаги по установке, сборке и запуску

### 1. Клонирование репозитория

Клонируйте репозиторий на свою локальную машину:

```bash
git clone https://github.com/AlexeyM01/wallet_sim
cd wallet_sim
```

### 2. Установка Docker и Docker Compose
Убедитесь, что Docker и Docker Compose установлены на вашем компьютере. Инструкции по установке [Docker](https://docs.docker.com/get-started/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

### 3. Настройка переменных окружения
Создайте файл .env в корневой директории проекта и добавьте необходимые переменные окружения:

```text
DB_HOST=db
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASS=your_password

```

### 4. Сборка и запуск контейнеров
Запустите следующую команду для сборки и запуска контейнеров:

```bash
docker-compose up --build
```

### 5. Создайте базу данных и заполните её
В корневом каталоге в командной строке напишите
```bash
alembic upgrade head
```

### 6. Проверка работы приложения
После успешного запуска контейнеров, перейдите по адресу ```http://localhost:8080``` в вашем веб-браузере

##Примеры использования
###Пример POST запроса для внесения или снятия средств с кошелька::

```http
POST /api/v1/wallets/<WALLET_UUID>/operation
Content-Type: application/json

{
  "operation_type": "DEPOSIT",  // или "WITHDRAW"
  "amount": 1000
}
```

##Пример GET запроса для получения баланса кошелька:

```http
GET /api/v1/wallets/{WALLET_UUID}
}
```

