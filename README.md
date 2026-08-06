# PlacePilot

**AI-powered Placement Preparation Ecosystem for students.**
*Learn. Practice. Build. Get Hired.*

PlacePilot brings learning roadmaps, coding practice, aptitude & interview prep,
a resume/ATS analyzer, skill-gap analysis, and an AI assistant into a single
dashboard, so students never have to switch between platforms.

## Tech Stack

- **Frontend:** React, Tailwind CSS, React Router, Axios, TanStack Query
- **Backend:** Django, Django REST Framework, PostgreSQL, SimpleJWT
- **Infra:** Docker, Docker Compose, GitHub Actions CI/CD
## Project Structure

```
placepilot/
├── backend/     # Django REST API (see backend/apps/*)
├── frontend/    # React SPA (see frontend/src/*)
├── nginx/       # Production reverse-proxy config
└── .github/     # CI workflow
```

See `docs/blueprint.md` (or the project blueprint shared separately) for the
full architecture, ER diagram, API design, RBAC matrix, and phased build plan.

## Getting Started (Development)

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
2. Start everything:
   ```bash
   docker compose up --build
   ```
3. Run initial migrations and create a superuser (in a new terminal):
   ```bash
   docker compose exec backend python manage.py migrate
   docker compose exec backend python manage.py createsuperuser
   ```
4. Open the app:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api/v1/
   - API docs (Swagger): http://localhost:8000/api/v1/docs/
   - Django admin: http://localhost:8000/admin/

## Environment Variables

See `.env.example` for the full list — Django secret key/debug/allowed hosts,
Postgres credentials, JWT lifetimes, CORS origins, AI provider selection and
keys, and the frontend API base URL.

## Running Tests

```bash
# Backend
docker compose exec backend pytest --cov=apps

# Frontend
docker compose exec frontend npm run test
```

## Production Deployment

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

This builds optimized images (Gunicorn + WhiteNoise for the backend, an Nginx-served
static build for the frontend) behind a single Nginx reverse proxy terminating
`/api` to the backend and everything else to the frontend build.

## Developer Workflow

- One Django app per bounded context (`apps/accounts`, `apps/roadmaps`, `apps/coding`, ...),
  each following `models → services → serializers → views → permissions → urls → tests`.
- One React feature folder per domain (`features/roadmaps`, `features/coding`, ...),
  each owning its own API calls, hooks, components, and pages.
- AI calls always go through `apps/ai_assistant/providers/` — never call a provider
  SDK directly from a view or another app.
- Every PR must pass `ruff check`, `pytest`, `eslint`, and frontend tests (see
  `.github/workflows/ci.yml`).


  

## Current Status

Phase 1 (project setup) is complete: Docker/Compose, Django project + all app
scaffolds, PostgreSQL, React + Tailwind frontend, JWT auth (register/login/refresh/
logout/me/password-reset), and CI. Remaining modules are built phase-by-phase per
the project blueprint.





--------------------------------------------------------------------------------------------------------------------
