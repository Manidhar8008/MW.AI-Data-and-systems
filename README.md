# MW.AI Data and Systems

MW.AI Data and Systems is a modular CRM and automation platform for Tier-2 Indian businesses. The first product direction is a lightweight, operational CRM with leads, tasks, follow-ups, WhatsApp-centric workflows, and automation that can be built by a small team without starting as microservices.

## Project Vision

Build a practical SaaS CRM for businesses in Warangal and similar markets:

- Capture and manage leads from phone, walk-ins, forms, WhatsApp, and referrals.
- Track daily tasks and follow-ups without forcing complex enterprise workflows.
- Add automation gradually after core CRM behavior is stable.
- Keep the codebase modular enough to scale, but simple enough for two developers to ship.

## Tech Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS
- Backend: FastAPI, Python, SQLAlchemy
- Database: PostgreSQL
- Auth: JWT-based starter architecture
- State and routing: Zustand, React Router
- HTTP client: Axios
- Future AI layer: provider-neutral interface, compatible with local Ollama first and optional API providers later
- Deployment: Docker-ready later, no Kubernetes or microservices in the initial architecture

## Architecture

```text
MW.AI-Data-and-systems/
├── backend/                         # FastAPI application and backend dependencies
│   ├── app/
│   │   ├── api/                     # API router composition and versioned route modules
│   │   ├── core/                    # Settings, logging, security, and cross-cutting config
│   │   ├── db/                      # SQLAlchemy engine, sessions, and declarative base
│   │   ├── middleware/              # Request middleware such as tenant isolation
│   │   ├── models/                  # SQLAlchemy database models
│   │   ├── schemas/                 # Pydantic request and response schemas
│   │   ├── services/                # Business logic separated from route handlers
│   │   ├── utils/                   # Small reusable helpers
│   │   └── main.py                  # FastAPI app factory and router registration
│   ├── tests/                       # Backend tests
│   ├── .env.example                 # Backend environment template
│   └── requirements.txt             # Python dependencies
├── frontend/                        # React + TypeScript + Vite application
│   ├── public/                      # Static public assets
│   ├── src/
│   │   ├── components/              # Reusable UI components
│   │   ├── hooks/                   # React hooks for data and UI behavior
│   │   ├── layouts/                 # Page shells and navigation layouts
│   │   ├── pages/                   # Route-level screens
│   │   ├── routes/                  # React Router configuration
│   │   ├── services/                # API clients and external service adapters
│   │   ├── store/                   # Zustand stores
│   │   ├── types/                   # Shared TypeScript types
│   │   └── utils/                   # Formatting and utility functions
│   ├── .env.example                 # Frontend environment template
│   └── package.json                 # Frontend dependencies and scripts
├── database/                        # Migration and seed organization
│   ├── migrations/                  # Alembic migration environment
│   └── seeds/                       # Local seed data and scripts
├── docker/                          # Future Docker assets, intentionally minimal now
├── docs/                            # Architecture, Git workflow, and roadmap notes
├── scripts/                         # Local setup and developer automation scripts
├── .github/                         # Pull request templates and future CI workflows
├── .env.example                     # Root environment reference
├── .gitignore                       # Git ignore rules for Python, Node, env, and local data
├── alembic.ini                      # Alembic configuration
└── README.md                        # Project overview and setup guide
```

## Local Setup

Run these commands in Windows PowerShell from the repository root.

### Backend

```powershell
cd "D:\MW.AI data & systems\MW.AI-Data-and-systems"
Copy-Item .\backend\.env.example .\backend\.env -Force
cd .\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend tests from the repository root:

```powershell
.\backend\.venv\Scripts\python.exe -m pytest
```

Backend health check:

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/api/v1/health"
```

Tenant-scoped CRM endpoints require `X-Tenant-ID`:

```powershell
Invoke-RestMethod `
  -Method Get `
  -Uri "http://127.0.0.1:8000/api/v1/leads" `
  -Headers @{ "X-Tenant-ID" = "local-demo-tenant" }
```

### Frontend

```powershell
cd "D:\MW.AI data & systems\MW.AI-Data-and-systems\frontend"
Copy-Item .\.env.example .\.env -Force
npm install
npm run dev
```

Frontend local URL:

```text
http://localhost:5173
```

### One-Command Local Dependency Setup

```powershell
cd "D:\MW.AI data & systems\MW.AI-Data-and-systems"
.\scripts\init-dev.ps1
```

## Fresh Bootstrap Commands

These are the equivalent commands for creating this structure from an empty repository. Do not run the Vite create command over an existing populated `frontend` directory.

```powershell
mkdir frontend, backend, docs, scripts, database, docker, .github
mkdir backend\app, backend\app\api, backend\app\api\routes, backend\app\models, backend\app\schemas, backend\app\services
mkdir backend\app\db, backend\app\core, backend\app\middleware, backend\app\utils, backend\tests
mkdir frontend\src, frontend\src\components, frontend\src\pages, frontend\src\layouts, frontend\src\hooks
mkdir frontend\src\services, frontend\src\store, frontend\src\utils, frontend\src\types, frontend\src\routes
mkdir database\migrations, database\seeds, .github\workflows

cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy asyncpg psycopg2-binary python-dotenv pydantic pydantic-settings alembic passlib[bcrypt] python-jose[cryptography] loguru

cd ..
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install react-router-dom axios zustand lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

cd ..
git init
git add .
git commit -m "chore: scaffold crm monorepo"
git branch -M main
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

## Git Workflow

Branch naming:

- `feature/auth-jwt-login`
- `feature/leads-crud`
- `fix/leads-tenant-filter`
- `chore/update-dependencies`
- `docs/git-workflow`

Commit naming:

- `feat: add lead creation endpoint`
- `fix: enforce tenant filter on lead queries`
- `chore: add frontend dependency setup`
- `docs: document local setup`
- `test: add health endpoint test`

Pull request workflow:

1. Create a short-lived branch from `main`.
2. Keep each PR focused on one module or workflow.
3. Include setup notes, screenshots for UI changes, and API examples for backend changes.
4. Request review from the other developer before merging.
5. Merge only after local tests pass and tenant scoping has been checked for data-access code.

Feature branch strategy:

- `main` stays stable and runnable.
- Developers work in feature branches.
- Rebase or merge from `main` before opening a PR if the branch is stale.
- Avoid long-running branches until the product modules are more mature.

## Contribution Guide

- Keep route handlers thin; put business rules in `backend/app/services`.
- Every tenant-owned database model must include `tenant_id`.
- Every tenant-owned query must filter by `tenant_id`.
- Do not add external AI providers directly into route handlers.
- Keep frontend API calls in `frontend/src/services`.
- Keep route-level UI in `frontend/src/pages` and reusable UI in `frontend/src/components`.
- Do not introduce microservices, Kubernetes, queues, or paid cloud dependencies until the MVP requires them.

## Roadmap

Phase 1:

- JWT authentication
- Leads module
- Tasks module
- Follow-up tracking
- Basic dashboard

Phase 2:

- WhatsApp integration
- Analytics views
- Role permissions
- Activity timeline

Phase 3:

- AI summaries
- Automation engine
- Workflow triggers
- Provider-neutral AI adapter for local Ollama first and optional external providers later
