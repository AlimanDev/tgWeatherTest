### Инструкция по запуску
> Создать .env файл в корне проекта (взять из .env_example)
#### Запуск через докер
```docker
docker compose up --build
```
#### Локальный запуск
> Добавить в .env: ```SERVER_DOMAIN=127.0.0.1```
```python
python backend/manage.py migrate
python backend/manage.py runserver
python tgbot/main.py
```