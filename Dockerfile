FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя без root прав (безопасность!)
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/static/uploads && \
    chown -R appuser:appuser /app

# Копирование requirements
COPY --chown=appuser:appuser requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY --chown=appuser:appuser . .

# Переключение на непривилегированного пользователя
USER appuser

EXPOSE 8000

# Health check для Docker
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Запуск с несколькими workers для production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]