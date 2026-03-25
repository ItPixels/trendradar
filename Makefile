.PHONY: dev dev-frontend dev-backend \
       install install-frontend install-backend \
       db-migrate db-upgrade db-downgrade \
       test test-frontend test-backend \
       lint lint-frontend lint-backend \
       docker-up docker-down \
       celery-worker celery-beat

# ── Development ──────────────────────────────────────────────

dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev:
	$(MAKE) -j2 dev-frontend dev-backend

# ── Install ──────────────────────────────────────────────────

install-frontend:
	cd frontend && npm install

install-backend:
	cd backend && pip install -r requirements.txt

install: install-frontend install-backend

# ── Database ─────────────────────────────────────────────────

db-migrate:
	cd backend && alembic revision --autogenerate -m "$(msg)"

db-upgrade:
	cd backend && alembic upgrade head

db-downgrade:
	cd backend && alembic downgrade -1

# ── Testing ──────────────────────────────────────────────────

test-frontend:
	cd frontend && npm run test

test-backend:
	cd backend && pytest

test: test-frontend test-backend

# ── Linting ──────────────────────────────────────────────────

lint-frontend:
	cd frontend && npm run lint

lint-backend:
	cd backend && ruff check . && ruff format --check .

lint: lint-frontend lint-backend

# ── Docker ───────────────────────────────────────────────────

docker-up:
	docker compose up -d

docker-down:
	docker compose down

# ── Celery ───────────────────────────────────────────────────

celery-worker:
	cd backend && celery -A app.celery_app worker --loglevel=info

celery-beat:
	cd backend && celery -A app.celery_app beat --loglevel=info
