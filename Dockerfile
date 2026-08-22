FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements/base.txt .
RUN pip install --no-cache-dir -r base.txt

COPY . .

# Run migrations and collect static
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# Create superuser
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
