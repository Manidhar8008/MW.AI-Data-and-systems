# Database

This folder keeps database migration and seed assets separate from the FastAPI application code.

- `migrations/`: Alembic migration environment and generated revisions.
- `seeds/`: local seed data or scripts for development fixtures.

Initial local database target:

```text
postgresql+asyncpg://mwai:mwai_password@localhost:5432/mwai_crm
```

Run Alembic from the repository root after backend dependencies are installed:

```powershell
.\backend\.venv\Scripts\Activate.ps1
alembic revision --autogenerate -m "create leads table"
alembic upgrade head
```

