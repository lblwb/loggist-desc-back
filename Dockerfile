# backend/Dockerfile

# Используем базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app/backend

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем все содержимое текущей директории внутрь контейнера
COPY . .

# Запускаем Django сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]