# Instructions pour Nova Task

## Structure du projet

```
├── backend/            # Django (API REST)
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/         # settings.py, urls.py, wsgi.py, asgi.py
│   └── tasks/          # app Django (modèles, vues, serializers)
├── frontend/           # Vue 3 + Vite + Tailwind
│   ├── package.json
│   ├── vite.config.js
│   └── src/
├── Dockerfile          # build multi-étapes (frontend + backend)
├── docker-compose.yml  # web + postgres, profil "https" (Caddy)
├── Caddyfile
└── .env.example
```

## Stack technique

- Backend : Django 6.0.3 + Django REST Framework + SQLite (dev) / PostgreSQL (prod)
- Auth : JWT (`djangorestframework-simplejwt`)
- Frontend : Vue 3 + Vite + Tailwind CSS v4
- Package settings Django : `config` (ROOT_URLCONF `config.urls`, WSGI `config.wsgi`)

## Commandes utiles

### Backend (depuis `backend/`)

Le venv Python se trouve à la racine du workspace :

```bash
../venv/Scripts/python.exe manage.py makemigrations
../venv/Scripts/python.exe manage.py migrate
../venv/Scripts/python.exe manage.py runserver
../venv/Scripts/python.exe manage.py check
```

### Frontend (depuis `frontend/`)

```bash
npm install
npm run dev
npm run build
```

### Déploiement (VPS, Docker)

Fichiers à la racine du dépôt : `Dockerfile`, `docker-compose.yml`, `Caddyfile`, `.env.example`.
En prod, Django sert la SPA buildée via WhiteNoise (`WHITENOISE_ROOT` → `frontend/dist`) + route catch-all dans `config/urls.py`.
Configuration par variables d'environnement : `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, `POSTGRES_*`.

## Points importants

- L'application supporte les entreprises (`Company`), les profils utilisateurs (`UserProfile`) avec rôles `ceo` / `employee`.
- Les tâches sont scopées par entreprise et peuvent être assignées à des employés.
- La suppression d'une tâche effectue un soft delete (corbeille via `/api/trash/`).
- Les notifications sont créées lors de l'assignation et du changement de statut.
- Le dashboard PDG expose des statistiques par employé.

## Fichiers clés

- `backend/tasks/models.py` : `Company`, `UserProfile`, champs `assigned_to` / `company` / `is_deleted` / `deleted_at`
- `backend/tasks/views.py` : permissions, `CompanyViewSet`, `EmployeeListAPIView`, `TaskViewSet`, `DashboardAPIView`, `TrashAPIView`, notifications
- `backend/tasks/serializers.py` : `TaskSerializer`, `CompanySerializer`, `UserSerializer`, `formatDuration`
- `backend/tasks/urls.py` : routes `/companies/`, `/employees/`, `/trash/`, `/notifications/unread/`, etc.
- `backend/tasks/permissions.py` : permissions multi-tenant et par rôle
- `backend/config/urls.py` : routes API + catch-all SPA
- Frontend : `Register.vue`, `Login.vue`, `kanban.vue`, `TaskDetail.vue`, `Company.vue`, `Notifications.vue`, `Archives.vue`, `TableauDeBord.vue`, `Sidebar.vue`, `Navbar.vue`, `router/index.js`
