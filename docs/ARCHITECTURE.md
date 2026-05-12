# Architecture

The repository starts as a modular monolith with a separate frontend and backend.

## Backend Boundaries

- `api/routes`: HTTP layer only. Validate inputs, call services, return schemas.
- `services`: business rules and tenant-scoped operations.
- `models`: database persistence shape.
- `schemas`: API contract shape.
- `db`: database engine, session lifecycle, and base metadata.
- `core`: configuration, logging, and security helpers.
- `middleware`: request-level controls such as tenant isolation.
- `utils`: small helpers that do not own business logic.

## Frontend Boundaries

- `pages`: route-level screens.
- `layouts`: navigation and page shells.
- `components`: reusable UI pieces.
- `services`: API clients and integration boundaries.
- `store`: shared client state.
- `hooks`: React composition helpers.
- `types`: shared TypeScript types.
- `utils`: formatting and local helpers.

## Tenant Isolation Rule

Tenant-owned data must include `tenant_id`.

Any query that reads, writes, updates, or deletes tenant-owned rows must be scoped by `tenant_id`. Missing tenant context is a defect, not a recoverable default.

