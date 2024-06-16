# Используем базовый образ Python
FROM python:3.10

# Установка переменной окружения PYTHONUNBUFFERED для вывода логов сразу
ENV PYTHONUNBUFFERED 1

# Создание директории приложения внутри контейнера
RUN mkdir /code

# Установка рабочей директории в контейнере
WORKDIR /code

# Копируем зависимости проекта (requirements.txt) в контейнер
COPY requirements.txt /code/

# Установка зависимостей через pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем все содержимое текущей директории в контейнер в директорию /code/
COPY . /code/
