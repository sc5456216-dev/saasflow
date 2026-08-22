FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements/base.txt .
RUN pip install --no-cache-dir -r base.txt

COPY . .

# Run migrations and collect static during build
RUN python manage.py migrate --noinput || true
RUN python manage.py collectstatic --noinput || true

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
