# TrendRadar — AI Agent Context

## What is TrendRadar?

TrendRadar is a Signal Intelligence platform that continuously monitors, analyzes, and surfaces emerging trends across industries. It collects weak signals from diverse data sources, clusters them into coherent trends, and presents actionable intelligence to decision-makers.

## Architecture Overview

The system follows a **Signal Intelligence** pipeline:

1. **Collection** — Ingest raw signals from APIs, feeds, and scrapers (news, patents, research papers, social media, job postings).
2. **Processing** — Clean, normalize, and enrich signals using NLP and LLM-based extraction.
3. **Analysis** — Cluster related signals into trends, score them by momentum and relevance, detect inflection points.
4. **Delivery** — Present trends via an interactive dashboard with radar visualizations, alerts, and reports.

## Tech Stack

- **Frontend**: Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: Python, FastAPI, SQLAlchemy, Alembic
- **Task Queue**: Celery with Redis broker
- **Database**: PostgreSQL 16
- **Cache / Broker**: Redis 7.2
- **Infrastructure**: Docker Compose (dev), containerized deployment (prod)

## Project Structure

```
trendradar/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── docker-compose.yml # Dev services (Postgres, Redis)
└── Makefile           # Common dev commands
```

## Key Conventions

- Backend uses Alembic for database migrations.
- Celery handles async signal collection and processing tasks.
- Environment variables are stored in `.env` (not committed).
- Use `make install` to set up both frontend and backend dependencies.
- Use `make dev` to start both dev servers concurrently.
