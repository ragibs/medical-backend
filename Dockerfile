FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1  # Avoid writing .pyc files
ENV PYTHONUNBUFFERED 1        # Output directly to stdout/stderr

WORKDIR /app

COPY MedAppBackend/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY MedAppBackend /app/

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "MedAppBackend.wsgi:application"]
