FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DEFAULT_TIMEOUT 100

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip==23.0.1 && \
    pip install -r requirements.txt --no-cache-dir

# Копирование проекта
COPY . .

CMD ["gunicorn", "citymap.wsgi:application", "--bind", "0.0.0.0:8000"]