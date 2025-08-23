source venv/bin/activate активация виртуального окружения ubuntu
pip install -r requirements установка зависимостей

docker-compose -up запуск БД в докере

python3 main.py запуск приложения
либо - uvicorn main:app --reload из папки src/app

alembic revision --autogenerate -m "" автоматическое создание таблицы
alembic upgrade head накатываем изменения на БД
