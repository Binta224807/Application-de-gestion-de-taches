# ---- Étape 1 : build du frontend Vue ----
FROM node:22-alpine AS frontend-build
WORKDIR /frontend
COPY GESTION_TACHES/frontend/package.json GESTION_TACHES/frontend/package-lock.json ./
RUN npm ci
COPY GESTION_TACHES/frontend/ ./
RUN npm run build

# ---- Étape 2 : backend Django ----
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY GESTION_TACHES/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY GESTION_TACHES/ .
COPY --from=frontend-build /frontend/dist ./frontend/dist

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn GESTION_TACHES.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
