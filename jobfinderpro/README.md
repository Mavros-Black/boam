# JobFinderPro

Production-ready app that scrapes jobs based on your resume & criteria, shows them in a dashboard, lets you apply with one click, and tracks application status.

## Monorepo Structure

```
/jobfinderpro
  /backend
  /frontend
  /infra
  README.md
```

## Prerequisites

- Docker and Docker Compose (recommended)
- Or: Python 3.11, Node.js 20+, npm or pnpm

## Quick Start (Docker)

1. Copy `.env.example` to `.env` and adjust if needed.
2. Build and run:

```bash
docker compose -f infra/docker-compose.yml up --build
```

- API: `http://localhost:8000` (docs at `/docs`)
- Frontend: `http://localhost:5173`
- Postgres: `localhost:5432` (user: postgres / pass: postgres)

Stop:
```bash
docker compose -f infra/docker-compose.yml down
```

## Quick Start (Local Dev)

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev -- --host
```

## Environment

Copy `.env.example` to `.env`. Environment variables:

```
# API
PORT=8000
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/jobfinderpro
ALLOWED_ORIGINS=http://localhost:5173

# Resume & identity for autofill (dev only)
RESUME_PATH=./infra/sample_resume.pdf
FULL_NAME=John Doe
EMAIL=john@example.com
PHONE=+233 20 000 0000

# Apply automation (toggle)
ENABLE_AUTOFILL=true
```

## ToS & Ethics

This project includes automation. Only use it on sites where it is permitted. Respect robots.txt and website ToS. For sites that disallow automation, restrict to opening the public apply URL and manual review.

## License

MIT