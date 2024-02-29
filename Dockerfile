# Используйте официальный образ Python как базовый
FROM python:3.9

# Установите рабочий каталог в контейнере
WORKDIR /app

# Скопируйте файл зависимостей и установите зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте остальную часть исходного кода проекта
COPY . .

# Команда для запуска приложения
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
