FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências antes de copiar o código, aproveitando o cache.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# A aplicação roda com um usuário sem privilégios de administrador.
RUN useradd --create-home app \
    && mkdir -p /app/media \
    && chown -R app:app /app
USER app

EXPOSE 8000

# Cria/atualiza as tabelas e inicia o servidor da aplicação.
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --access-logfile - --error-logfile -"]
