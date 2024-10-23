# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY web-app-code.py /app/

# Устанавливаем Nginx и необходимые инструменты
RUN apt-get update && apt-get install -y nginx

# Копируем конфигурацию Nginx
COPY nginx-config.txt /etc/nginx/sites-available/flask-app
RUN ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/

# Удаляем дефолтный сайт
RUN rm /etc/nginx/sites-enabled/default

# Запускаем Nginx и Flask на порту 5000
CMD service nginx start && python web-app-code.py

# Открываем порт 5000 для Flask
EXPOSE 5000
