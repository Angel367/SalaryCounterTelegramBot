FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY salary_bot.py .

# Создание непривилегированного пользователя
RUN useradd -m -u 1000 botuser
USER botuser

# Запуск бота
CMD ["python", "salary_bot.py"]