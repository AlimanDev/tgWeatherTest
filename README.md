### Инструкция по запуску
1. Создать virtualenv (python >= 3.10)
2. Установить зависимости из requirements.txt
3. Создать .env файл (взять из .env_example)
4. Запустить backend ```python backend/manage.py runserver```
5. Запустить миграцию ```python backend/manage.py migrate```
6. Запустить тесты ```python backend/manage.py test```
7. Запустить tgbot ```python tgbot/main.py```