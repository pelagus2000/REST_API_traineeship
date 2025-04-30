# ФСТР Перевал API
## Описание проекта
Проект API для Федерации Спортивного Туризма России (ФСТР) для ведения базы горных перевалов, пополняемой туристами. Данный API используется мобильными приложениями для Android и iOS, позволяющими туристам отправлять данные о пройденных перевалах.
## Функциональные возможности
- Добавление новой информации о перевалах (координаты, фотографии, название и т.д.)
- Просмотр детальной информации о перевале
- Редактирование информации о перевале (если статус "new")
- Просмотр всех перевалов, добавленных конкретным пользователем
- Модерация добавленных данных (для администраторов)
- Поиск и фильтрация перевалов по различным параметрам

## Структура проекта
Проект построен на Django и Django REST Framework и состоит из следующих основных приложений:
- `pereval` - основное приложение для работы с перевалами
- `tourist` - приложение для управления данными о туристах
- `coordinates` - приложение для хранения и управления географическими координатами 
- `photo` - приложение для хранения и управления фотографиями

## Модели данных
### Pereval (Перевал)
- beauty_title - сокращенное название перевала
- title - полное название перевала
- other_titles - альтернативное название
- connect - информация о том, что соединяет перевал
- created - дата и время добавления
- level - уровень сложности (сезонно)
- status - статус модерации (new, pending, accepted, rejected)
- area - географическая область
- tourist - связь с моделью Tourist
- coords - связь с моделью Coords
- photo - связь с моделью Image

### Tourist (Турист)
- email - адрес электронной почты туриста
- fam - фамилия
- name - имя
- otc - отчество
- phone - телефон
- type - вид туризма

### Coords (Координаты)
- latitude - широта
- longitude - долгота
- height - высота над уровнем моря

### Image (Изображение)
- photo - файл изображения
- title - название изображения
- created - дата создания

## API Endpoints
### Добавление нового перевала
- **URL**: `/api/v1/submitData/`
- **Метод**: POST
- **Описание**: Создает новую запись о перевале

### Получение деталей перевала
- **URL**: `/api/v1/pereval/<id>/`
- **Метод**: GET
- **Описание**: Возвращает детальную информацию о перевале по его ID

### Редактирование перевала
- **URL**: `/api/v1/submitData/<id>/`
- **Метод**: PATCH
- **Описание**: Позволяет редактировать данные перевала (только если статус "new")

### Получение списка перевалов пользователя
- **URL**: `/api/v1/pereval/user/?user__email=<email>`
- **Метод**: GET
- **Описание**: Возвращает список всех перевалов, добавленных пользователем с указанным email

### Модерация перевала
- **URL**: `/api/v1/pereval/<id>/moderate/`
- **Метод**: PATCH
- **Описание**: Позволяет модераторам изменять статус перевала

### Поиск перевалов
- **URL**: `/api/v1/pereval/search/`
- **Метод**: GET
- **Описание**: Позволяет искать и фильтровать перевалы по различным параметрам

## Документация API
Документация доступна по следующим URL:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Установка и запуск
### Требования
- Python 3.8+
- PostgreSQL

### Установка
1. Клонировать репозиторий:
``` bash
git clone https://github.com/yourusername/fstr-pereval-api.git
cd fstr-pereval-api
```
2. Создать и активировать виртуальное окружение:
``` bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate     # для Windows
```
3. Установить зависимости:
``` bash
pip install -r requirements.txt
```
4. Настроить переменные окружения:
``` bash
export FSTR_DB_HOST=your_db_host
export FSTR_DB_PORT=your_db_port
export FSTR_DB_LOGIN=your_db_login
export FSTR_DB_PASS=your_db_password
```
5. Применить миграции:
``` bash
python manage.py migrate
```
6. Запустить сервер:
``` bash
python manage.py runserver
```
# Описание тестов для документации проекта

## Тесты системы

В нашем проекте реализована комплексная система тестирования, включающая модульные тесты моделей, сериализаторов и представлений. Эти тесты обеспечивают надежную работу API и помогают предотвратить регрессии при разработке.

### Тесты моделей

```python
python manage.py test pereval.tests.test_models
```


Тесты моделей проверяют корректность работы моделей данных, включая:

- **PerevalModelTest**: Тесты для модели перевалов, проверяющие корректность создания объектов, связей с другими моделями и строкового представления.
- **TermsAgreementModelTest**: Тесты модели согласия с условиями, включая проверку создания токенов и их статусов.
- **NotificationModelTest**: Тесты модели уведомлений, проверяющие создание уведомлений и порядок их сортировки.

### Тесты сериализаторов

```python
python manage.py test pereval.tests.test_serializers
```


Тесты сериализаторов обеспечивают корректную валидацию и преобразование данных:

- **PerevalSerializerTest**: Проверяет работу сериализатора перевалов, включая валидацию данных, обработку обязательных полей и проверку токенов согласия.
- **ModerationSerializerTest**: Тестирует сериализатор модерации, проверяя валидацию статусов перевалов.

### Тесты представлений

```python
python manage.py test pereval.tests.test_views
```


Тесты представлений проверяют работу API-эндпоинтов:

- **PerevalViewSetTest**: Тестирует работу API для перевалов, включая:
  - Фильтрацию перевалов по email пользователя
  - Частичное обновление перевала (PATCH-запросы)
  - Полное обновление перевала (PUT-запросы)

- **NotificationTest**: Проверяет систему уведомлений:
  - Создание уведомлений при изменении статуса перевала
  - Создание уведомлений при добавлении комментариев модератора

## Запуск всех тестов

Для запуска всех тестов используйте команду:

```python
python manage.py test pereval
```


## Тестовое покрытие

Тесты охватывают основные компоненты приложения:

1. **Модели данных**: проверка корректного создания и взаимодействия объектов
2. **Сериализаторы**: валидация входных данных, преобразование объектов
3. **API-эндпоинты**: корректная обработка HTTP-запросов, возвращение правильных ответов

## Результаты тестирования

После запуска тестов вы увидите отчет о выполнении, включающий:
- Количество тестов
- Время выполнения
- Информацию о пройденных и непройденных тестах

Если все тесты проходят успешно, это гарантирует корректную работу API перевалов и связанных компонентов системы.
OpenAPI_SPECS
{"swagger": "2.0", "info": {"title": "Pereval API", "description": "API для работы с перевалами", "termsOfService": "https://www.google.com/policies/terms/", "contact": {"email": "contact@pereval.local"}, "license": {"name": "BSD License"}, "version": "v1"}, "host": "127.0.0.1:8000", "schemes": ["http"], "basePath": "/api/v1", "consumes": ["application/json"], "produces": ["application/json"], "securityDefinitions": {"Basic": {"type": "basic"}}, "security": [{"Basic": []}], "paths": {"/pereval/search/": {"get": {"operationId": "pereval_search_list", "description": "", "parameters": [{"name": "search", "in": "query", "description": "A search term.", "required": false, "type": "string"}, {"name": "ordering", "in": "query", "description": "Which field to use when ordering the results.", "required": false, "type": "string"}, {"name": "page", "in": "query", "description": "A page number within the paginated result set.", "required": false, "type": "integer"}], "responses": {"200": {"description": "", "schema": {"required": ["count", "results"], "type": "object", "properties": {"count": {"type": "integer"}, "next": {"type": "string", "format": "uri", "x-nullable": true}, "previous": {"type": "string", "format": "uri", "x-nullable": true}, "results": {"type": "array", "items": {"$ref": "#/definitions/PerevalList"}}}}}}, "tags": ["pereval"]}, "parameters": []}, "/pereval/user/": {"get": {"operationId": "pereval_user_list", "description": "", "parameters": [{"name": "page", "in": "query", "description": "A page number within the paginated result set.", "required": false, "type": "integer"}], "responses": {"200": {"description": "", "schema": {"required": ["count", "results"], "type": "object", "properties": {"count": {"type": "integer"}, "next": {"type": "string", "format": "uri", "x-nullable": true}, "previous": {"type": "string", "format": "uri", "x-nullable": true}, "results": {"type": "array", "items": {"$ref": "#/definitions/PerevalList"}}}}}}, "tags": ["pereval"]}, "parameters": []}, "/pereval/{id}/": {"get": {"operationId": "pereval_read", "description": "", "parameters": [], "responses": {"200": {"description": "", "schema": {"$ref": "#/definitions/PerevalDetail"}}}, "tags": ["pereval"]}, "parameters": [{"name": "id", "in": "path", "description": "A unique integer value identifying this Перевал.", "required": true, "type": "integer"}]}, "/pereval/{id}/moderate/": {"put": {"operationId": "pereval_moderate_update", "description": "", "parameters": [{"name": "data", "in": "body", "required": true, "schema": {"$ref": "#/definitions/Moderation"}}], "responses": {"200": {"description": "", "schema": {"$ref": "#/definitions/Moderation"}}}, "tags": ["pereval"]}, "patch": {"operationId": "pereval_moderate_partial_update", "description": "", "parameters": [{"name": "data", "in": "body", "required": true, "schema": {"$ref": "#/definitions/Moderation"}}], "responses": {"200": {"description": "", "schema": {"$ref": "#/definitions/Moderation"}}}, "tags": ["pereval"]}, "parameters": [{"name": "id", "in": "path", "description": "A unique integer value identifying this Перевал.", "required": true, "type": "integer"}]}, "/submitData/": {"get": {"operationId": "submitData_list", "description": "", "parameters": [{"name": "page", "in": "query", "description": "A page number within the paginated result set.", "required": false, "type": "integer"}], "responses": {"200": {"description": "", "schema": {"required": ["count", "results"], "type": "object", "properties": {"count": {"type": "integer"}, "next": {"type": "string", "format": "uri", "x-nullable": true}, "previous": {"type": "string", "format": "uri", "x-nullable": true}, "results": {"type": "array", "items": {"$ref": "#/definitions/PerevalList"}}}}}}, "tags": ["submitData"]}, "post": {"operationId": "submitData_create", "description": "", "parameters": [{"name": "data", "in": "body", "required": true, "schema": {"$ref": "#/definitions/Pereval"}}], "responses": {"201": {"description": "", "schema": {"$ref": "#/definitions/Pereval"}}}, "tags": ["submitData"]}, "parameters": []}, "/submitData/user_submitted/": {"get": {"operationId": "submitData_user_submitted", "description": "", "parameters": [{"name": "page", "in": "query", "description": "A page number within the paginated result set.", "required": false, "type": "integer"}], "responses": {"200": {"description": "", "schema": {"required": ["count", "results"], "type": "object", "properties": {"count": {"type": "integer"}, "next": {"type": "string", "format": "uri", "x-nullable": true}, "previous": {"type": "string", "format": "uri", "x-nullable": true}, "results": {"type": "array", "items": {"$ref": "#/definitions/Pereval"}}}}}}, "tags": ["submitData"]}, "parameters": []}, "/submitData/{id}/": {"get": {"operationId": "submitData_read", "description": "", "parameters": [], "responses": {"200": {"description": "", "schema": {"$ref": "#/definitions/Pereval"}}}, "tags": ["submitData"]}, "put": {"operationId": "submitData_update", "description": "", "parameters": [{"name": "data", "in": "body", "required": true, "schema": {"$ref": "#/definitions/Pereval"}}], "responses": {"200": {"description": "", "schema": {"$ref": "#/definitions/Pereval"}}}, "tags": ["submitData"]}, "patch": {"operationId": "submitData_partial_update", "description": "", "parameters": [{"name": "data", "in": "body", "required": true, "schema": {"$ref": "#/definitions/PerevalUpdate"}}], "responses": {"200": {"description": "", "schema": {"$ref": "#/definitions/PerevalUpdate"}}}, "tags": ["submitData"]}, "delete": {"operationId": "submitData_delete", "description": "", "parameters": [], "responses": {"204": {"description": ""}}, "tags": ["submitData"]}, "parameters": [{"name": "id", "in": "path", "description": "A unique integer value identifying this Перевал.", "required": true, "type": "integer"}]}}, "definitions": {"PerevalList": {"required": ["title"], "type": "object", "properties": {"id": {"title": "ID", "type": "integer", "readOnly": true}, "title": {"title": "Полное название", "type": "string", "maxLength": 255, "minLength": 1}, "beauty_title": {"title": "Сокращенное название", "type": "string", "maxLength": 255}, "status": {"title": "Status", "type": "string", "readOnly": true, "minLength": 1}, "created": {"title": "Время добавления", "type": "string", "format": "date-time", "readOnly": true}}}, "Coords": {"required": ["latitude", "longitude", "height"], "type": "object", "properties": {"latitude": {"title": "Широта", "type": "number"}, "longitude": {"title": "Долгота", "type": "number"}, "height": {"title": "Высота", "type": "integer", "maximum": 9223372036854775807, "minimum": -9223372036854775808}}}, "Tourist": {"required": ["email", "fam", "name", "otc", "phone"], "type": "object", "properties": {"id": {"title": "ID", "type": "integer", "readOnly": true}, "email": {"title": "Электронная почта", "type": "string", "format": "email", "maxLength": 255, "minLength": 1}, "fam": {"title": "Фамилия", "type": "string", "maxLength": 255, "minLength": 1}, "name": {"title": "Имя", "type": "string", "maxLength": 255, "minLength": 1}, "otc": {"title": "Отчество", "type": "string", "maxLength": 255, "minLength": 1}, "phone": {"title": "Телефон", "type": "string", "maxLength": 20, "minLength": 1}, "type": {"title": "Вид туризма", "type": "string", "enum": ["walking", "skiing", "catamaran", "kayak", "ferry", "rafting", "cycling", "auto", "moto", "sail", "horseback"]}}}, "Image": {"required": ["title"], "type": "object", "properties": {"photo": {"title": "Изображение", "type": "string", "readOnly": true, "format": "uri"}, "title": {"title": "Название", "type": "string", "maxLength": 255, "minLength": 1}}}, "PerevalDetail": {"required": ["coords", "title"], "type": "object", "properties": {"id": {"title": "ID", "type": "integer", "readOnly": true}, "coords": {"$ref": "#/definitions/Coords"}, "tourist": {"$ref": "#/definitions/Tourist"}, "photo": {"$ref": "#/definitions/Image"}, "beauty_title": {"title": "Сокращенное название", "type": "string", "maxLength": 255}, "title": {"title": "Полное название", "type": "string", "maxLength": 255, "minLength": 1}, "other_titles": {"title": "Альтернативное название", "type": "string", "maxLength": 255}, "connect": {"title": "Соединяет", "type": "string", "maxLength": 255}, "created": {"title": "Время добавления", "type": "string", "format": "date-time", "readOnly": true}, "level": {"title": "Уровень сложности", "type": "string", "enum": ["winter", "summer", "autumn", "spring"]}, "status": {"title": "Статус", "type": "string", "enum": ["new", "pending", "accepted", "rejected"]}, "area": {"title": "Область", "type": "string", "enum": ["Planet Earth", "Pamiro-Alai", "Altay", "Nothern-Chuiskiy Ridge", "Southern-Chuiskiy Ridge", "Katun Ridge", "Fansky mountains", "Gussarskiy Ridge(west from The Anzob Pass)", "Matchinskiy mountain knot", "Takali mountain knot-Turkestan ridge", "High Alay", "Kichik-Alay and Eastern Alay", "Aladaglar", "Tavr", "Sayan mountains", "Listvyaga Ridge", "Ivanovsky Ridge", "Mungun-Taiga massif", "Tsagan-Shibetu Ridge", "Chikhachev Ridge (Sailugem)", "Shapshalsky Ridge", "Southern Altai Ridge", "Mongolian Altai Ridge", "Western Sayan", "Eastern Sayan", "Kuznetsky Alatau", "Kurai ridge"]}}}, "Moderation": {"type": "object", "properties": {"status": {"title": "Статус", "type": "string", "enum": ["new", "pending", "accepted", "rejected"]}}}, "Pereval": {"required": ["title", "tourist", "coords", "photo", "terms_token"], "type": "object", "properties": {"id": {"title": "ID", "type": "integer", "readOnly": true}, "beauty_title": {"title": "Сокращенное название", "type": "string", "maxLength": 255}, "title": {"title": "Полное название", "type": "string", "maxLength": 255, "minLength": 1}, "other_titles": {"title": "Альтернативное название", "type": "string", "maxLength": 255}, "connect": {"title": "Соединяет", "type": "string", "maxLength": 255}, "level": {"title": "Уровень сложности", "type": "string", "enum": ["winter", "summer", "autumn", "spring"]}, "status": {"title": "Статус", "type": "string", "enum": ["new", "pending", "accepted", "rejected"], "readOnly": true}, "area": {"title": "Область", "type": "string", "enum": ["Planet Earth", "Pamiro-Alai", "Altay", "Nothern-Chuiskiy Ridge", "Southern-Chuiskiy Ridge", "Katun Ridge", "Fansky mountains", "Gussarskiy Ridge(west from The Anzob Pass)", "Matchinskiy mountain knot", "Takali mountain knot-Turkestan ridge", "High Alay", "Kichik-Alay and Eastern Alay", "Aladaglar", "Tavr", "Sayan mountains", "Listvyaga Ridge", "Ivanovsky Ridge", "Mungun-Taiga massif", "Tsagan-Shibetu Ridge", "Chikhachev Ridge (Sailugem)", "Shapshalsky Ridge", "Southern Altai Ridge", "Mongolian Altai Ridge", "Western Sayan", "Eastern Sayan", "Kuznetsky Alatau", "Kurai ridge"]}, "tourist": {"$ref": "#/definitions/Tourist"}, "coords": {"$ref": "#/definitions/Coords"}, "photo": {"$ref": "#/definitions/Image"}, "terms_token": {"title": "Terms token", "type": "string", "minLength": 1}}}, "PerevalUpdate": {"required": ["title"], "type": "object", "properties": {"beauty_title": {"title": "Сокращенное название", "type": "string", "maxLength": 255}, "title": {"title": "Полное название", "type": "string", "maxLength": 255, "minLength": 1}, "other_titles": {"title": "Альтернативное название", "type": "string", "maxLength": 255}, "connect": {"title": "Соединяет", "type": "string", "maxLength": 255}, "level": {"title": "Уровень сложности", "type": "string", "enum": ["winter", "summer", "autumn", "spring"]}, "area": {"title": "Область", "type": "string", "enum": ["Planet Earth", "Pamiro-Alai", "Altay", "Nothern-Chuiskiy Ridge", "Southern-Chuiskiy Ridge", "Katun Ridge", "Fansky mountains", "Gussarskiy Ridge(west from The Anzob Pass)", "Matchinskiy mountain knot", "Takali mountain knot-Turkestan ridge", "High Alay", "Kichik-Alay and Eastern Alay", "Aladaglar", "Tavr", "Sayan mountains", "Listvyaga Ridge", "Ivanovsky Ridge", "Mungun-Taiga massif", "Tsagan-Shibetu Ridge", "Chikhachev Ridge (Sailugem)", "Shapshalsky Ridge", "Southern Altai Ridge", "Mongolian Altai Ridge", "Western Sayan", "Eastern Sayan", "Kuznetsky Alatau", "Kurai ridge"]}}}}}
