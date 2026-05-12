# Git Workflow

## Branches

- `main`: stable branch.
- `feature/<module>-<short-description>`: new product behavior.
- `fix/<module>-<short-description>`: bug fixes.
- `chore/<short-description>`: tooling, dependency, or setup work.
- `docs/<short-description>`: documentation-only changes.

Examples:

- `feature/leads-crud`
- `feature/auth-jwt-login`
- `fix/leads-tenant-filter`
- `chore/add-alembic`
- `docs/local-setup`

## Commits

Use short conventional commit messages:

- `feat: add lead creation endpoint`
- `fix: enforce tenant scope on lead list`
- `chore: add frontend routing`
- `docs: document git workflow`
- `test: add health route test`

## Pull Requests

Each pull request should include:

- What changed.
- How it was tested.
- Any new environment variables.
- Screenshots for visible frontend changes.
- API examples for backend endpoint changes.

Keep PRs small enough for one reviewer to understand in one pass.

