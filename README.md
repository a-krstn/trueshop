# Shop

## Содержание
- [О проекте](#о-проекте)
- [Стек](#стек)
- [Начало работы](#начало-работы)

## Стек
- Django
- PostgreSQL
- Redis
- Celery
- Flower
- HTML/CSS

## Начало работы
1. **Клонирование приложения**<br>
   `git clone git@github.com:a-krstn/trueshop.git`
2. **Создание виртуального окружения и его активация**<br>
   В командной строке из директории проекта<br>
   `python -m venv .venv`<br>
   - Windows: `.venv\Scripts\activate`<br>
   - Linux/MacOS: `source .venv/bin/activate`
3. **Установка зависимостей**<br>
   `pip install -r webdev\requirements.txt`
4. **Определение переменных среды**<br>
   Для успешного запуска приложения требуется создать файл .env
   в корневой папке проекта и определить в нем переменные среды. Перечень требуемых переменных
   перечислен в файле .env.example.<br>
5. **Запуск**<br>
   Выполнить команду `docker compose up`.<br>
   Приложение будет доступно по адресу http://localhost/

