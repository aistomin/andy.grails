# AGENTS.md — Andy Grails Project Guide

This file onboards AI agents to the andy.grails project.
If `AGENTS.local.md` is present in the repo root, read it — it contains personal workflow preferences and local environment details for the current developer.

---

## Why We Build This

Andy Grails is a personal music website for the scenic pseudonym "Andy Grails". The project serves two equally important purposes:

1. **A real artistic platform** — to showcase and stream music, eventually live at https://andy-grails.de
2. **A learning playground** — hands-on practice with a modern full-stack architecture using real-world tools and workflows

Built from scratch for full ownership and control — no third-party platform limits, no vendor lock-in.

---

## Project Structure

The project spans three GitHub repositories:

| Repo | Purpose |
|------|---------|
| [`aistomin/andy.grails`](https://github.com/aistomin/andy.grails) | Parent/wrapper: orchestration, E2E tests, deployment scripts |
| [`aistomin/andy.grails.backend`](https://github.com/aistomin/andy.grails.backend) | Java Spring Boot backend: REST API, data, media metadata |
| [`aistomin/andy.grails.frontend`](https://github.com/aistomin/andy.grails.frontend) | Angular frontend: UI, client logic, user experience |

The backend and frontend are Git submodules of the parent repo. Submodules do **not** need to be initialized to run the app with Docker — scripts pull images directly from Docker Hub using revision-based tags.

### Issue Tracking & Milestones

Each repo has its own GitHub issue tracker and milestones. Always check the relevant repo when working on a feature.

Current active milestone across all repos: **Version 1.0** (target: Sept 2026 backend / Jan 2027 frontend).
A **Backlog** milestone exists in each repo for unplanned ideas.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Java 21, Spring Boot 4.1, Maven, PostgreSQL 18 |
| Backend libs | JPA/Hibernate, Lombok, MapStruct, OpenAPI/Swagger, Testcontainers |
| Frontend | Angular 22, TypeScript 6, npm |
| Frontend testing | Jest, Puppeteer |
| E2E testing | Playwright 1.59 (lives in `playwright/` in parent repo) |
| Infrastructure | Docker, Docker Compose, nginx, Docker Hub (`andygrails/` org) |

---

## CI/CD Pipeline

Production deployment is not yet set up (see issues [#5](https://github.com/aistomin/andy.grails/issues/5), [#16](https://github.com/aistomin/andy.grails/issues/16), [#31](https://github.com/aistomin/andy.grails/issues/31)). The current automated pipeline:

```
Push to submodule master
  → CI: unit tests + build (Maven for backend / Jest + prod Docker smoke test for frontend)
  → Docker image pushed to Docker Hub:
      andygrails/andy-grails-backend:<sha_short>
      andygrails/andy-grails-frontend:<sha_short>
  → repository_dispatch event sent to parent repo
  → Parent repo: updates submodule ref, runs Playwright E2E tests
  → If E2E pass: commits updated submodule ref to parent master
```

Pull requests to master run tests but do **not** publish Docker images or trigger parent updates.

### Key Scripts (parent repo root)

| Script | Purpose |
|--------|---------|
| `./start.sh` | Start full stack (frontend + backend + DB) via Docker Compose |
| `./stop.sh` | Stop all containers |
| `./deploy.sh <revision>` | Deploy to a specific git SHA, branch, or tag |
| `./run-e2e-tests.sh` | Run Playwright E2E tests (app must already be running) |

---

## Technical Idiosyncrasies

- **Submodules not needed for Docker runs** — `start.sh` resolves the current git revision and pulls the matching Docker Hub image tag directly.
- **Revision-based image tags** — images are tagged with the short git SHA (e.g. `andygrails/andy-grails-backend:abc1234`). The `latest` tag is also pushed on every master build.
- **Database defaults** — `DB_NAME=andy_grails`, `DB_USER=andy`, `DB_PASSWORD=andy`. Override via env vars.
- **E2E base URL** — defaults to `http://localhost:4200`. Override with `PLAYWRIGHT_BASE_URL`.
- **Coverage** — backend coverage reports go to Codecov automatically on master pushes.
- **Docker Hub cleanup** — runs daily at 3 AM UTC, retains the latest 10 tags per repository (`scripts/dockerhub_cleanup.py`).
- **Access URLs** — frontend: `http://localhost:4200`, backend API: `http://localhost:8080`, database: `localhost:55432`.
