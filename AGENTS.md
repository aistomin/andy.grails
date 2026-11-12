# AGENTS.md — Andy Grails Project Guide

This file onboards AI agents to the andy.grails project.
If `AGENTS.local.md` is present in the repo root, read it — it contains personal preferences and local environment details for the current developer. It is gitignored; create it by copying `AGENTS.local.md.template`.

**This file is the single source of truth for project conventions.** Agents must record any project-level convention, principle, or agreement here (via a normal reviewed change), never in an agent's private memory or other machine-local storage — a fresh clone of this repo must be enough to onboard anyone, human or AI. Machine-specific details go to `AGENTS.local.md`.

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

Current active milestone across all repos: **Version 1.0** (due 2027-01-01 in all three repos).
A **Backlog** milestone exists in each repo for unplanned ideas.

**Cross-repo changes:** the lead issue lives in the repo the technical change comes from and carries the full rationale; each other repo that must adapt gets a short follow-up issue linking back to the lead. Example: removing Spring profiles is led by [backend#299](https://github.com/aistomin/andy.grails.backend/issues/299), while [parent#97](https://github.com/aistomin/andy.grails/issues/97) merely adopts `docker-compose.yml`.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Java 25, Spring Boot 4.1, Maven, PostgreSQL 18 |
| Backend libs | JPA/Hibernate, Lombok, MapStruct, OpenAPI/Swagger, Testcontainers |
| Frontend | Angular 22, TypeScript 6, npm |
| Frontend testing | Jest, Puppeteer |
| E2E testing | Playwright (lives in `playwright/` in parent repo) |
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

Pull requests to master run tests (in the parent repo: the Playwright E2E tests) but do **not** publish Docker images or trigger parent updates.

### Key Scripts (parent repo root)

| Script | Purpose |
|--------|---------|
| `./start.sh` | Start full stack (frontend + backend + DB) via Docker Compose |
| `./stop.sh` | Stop all containers |
| `./deploy.sh <revision>` | Deploy to a specific git SHA, branch, or tag |
| `./run-e2e-tests.sh` | Run Playwright E2E tests (app must already be running) |

---

## Configuration Philosophy

**One project, one file, one configuration point.** This is a tiny, low-load, non-commercial system: redeploys take minutes and downtime is cheap, while config sprawl (parameters nobody understands anymore) is a real, permanent cost.

- **No dev/prod profiles.** Development, Docker, and production run the identical base configuration (`application.yml` in the backend). Environments may differ in *data* (hosts, credentials — via env vars), never in *behavior*.
- **Every parameter must be "written in blood."** Add a config parameter only after a real problem demanded it — never preemptively, never "because it's best practice". Prefer hardcoded values over env vars and tunables until tuning without redeploy is an actual, experienced need.
- **Temporary debugging toggles are not configuration.** Use Spring's relaxed binding ad hoc (e.g. `SPRING_JPA_SHOW_SQL=true`) instead of adding entries to config files.

---

## Technical Idiosyncrasies

- **Submodules not needed for Docker runs** — `start.sh` resolves the current git revision and pulls the matching Docker Hub image tag directly.
- **Revision-based image tags** — images are tagged with the short git SHA (e.g. `andygrails/andy-grails-backend:abc1234`). The `latest` tag is also pushed on every master build.
- **Database defaults (Docker Compose)** — `DB_NAME=andy_grails`, `DB_USER=andy`, `DB_PASSWORD=andy`. Override via env vars.
- **E2E base URL** — defaults to `http://localhost:4200`. Override with `PLAYWRIGHT_BASE_URL`.
- **Coverage** — backend coverage reports go to Codecov on every CI run, pull requests included.
- **Docker Hub cleanup** — runs daily at 3 AM UTC, retains the latest 10 tags per repository plus every submodule revision referenced by the last 30 parent master commits, so the deployed images and recent rollback targets stay pullable (`scripts/dockerhub_cleanup.py`).
- **Access URLs** — frontend: `http://localhost:4200`, backend API: `http://localhost:8080`, database: `localhost:55432`.

---

## Workflow

All work is issue-driven. The owner keeps full control over the git history; the agent never acts on git on its own initiative.

1. The owner provides a GitHub issue number.
2. The agent pulls the latest master in the parent repo, updates the submodule refs, and pulls the latest master in the working copy of every repo the issue may touch (local paths are in `AGENTS.local.md`).
3. The agent reads the issue from GitHub, including its comments, and grills the owner until the requirements are clear (use the `grill-me` skill if available). If the issue's claimed problem no longer holds, say so before anything else.
4. Agent and owner iterate on a plan — the plan determines which repo(s) are touched.
5. The agent creates a feature branch `Issue-<number>` in each touched repo (e.g. issue #123 → `Issue-123`), using that repo's own issue number. A commit never references an issue from another repo, so every touched repo needs its own issue (see [Cross-repo changes](#issue-tracking--milestones)).
6. The owner explicitly says "go" — only then does the agent touch any file. Before the first edit, check with `git branch --show-current` that the branch matches the issue.
7. The agent verifies the change — see [Verification](#verification).
8. The owner reviews; the agent proposes a commit message — see [Commits](#commits).
9. The agent commits only when the owner says "commit", and pushes only when the owner says "push".
10. Always suggest the next step, never perform it: after committing, offer to push; after pushing, offer to create the pull request and propose its title. The suggestion is a prompt, not permission to act.

---

## Verification

A change is ready to commit only when every step of the "How to Contribute" section in the affected repo's README has actually passed. For the frontend, that includes checking the change in a browser in both the dev and the prod setup.

If a step cannot run (Docker is down, a tool is missing, a command fails), say so plainly and stop. Never propose a commit message or report the work as done while any step is still open.

The backend build uses Testcontainers and the parent's E2E tests run against the Docker stack, so check that Docker is running (`docker info`) before starting either; if it is not, ask the owner to start it.

---

## Commits

- Commit messages and pull request titles follow [Conventional Commits](https://www.conventionalcommits.org/), with the issue number as the scope in the first line, e.g. `fix(#252): hide actuator health details`.
- No AI attribution: no `Co-Authored-By` trailer for an agent, no "Generated with ..." line, in neither commit messages nor pull request bodies.
- Only the explicit word authorizes a git action: "commit", "push", "create the PR". Agreement with the reasoning, a joke, or a "yeah" is not a go — ask again. An explicit "push" needs no further confirmation.
- Force-pushing always needs its own explicit go; it never inherits permission from an earlier approval.

---

## Issues

- **Check for duplicates first.** Before proposing an issue, search the existing issues of all three repos and mention anything related or overlapping.
- **A ticket needs a payoff.** Propose work only when you can name what the owner would feel: a bug that would bite, a change that gets easier, a risk that gets closed. "It's cleaner" or "it's unused" is not a payoff on its own.
- **Draft, then create.** Present the full issue text (title and body, exactly as it would be posted) and ask "create or skip?". Create it only after the owner agrees.
- **Title** — a plain, human-readable sentence, e.g. "Mask forbidden words in chat messages". Never Conventional Commits format.
- **Assignee** — always the repo owner, `aistomin`.
- **Milestone** — always the repo's current active milestone (see [Issue Tracking & Milestones](#issue-tracking--milestones)).
- **Footer** — end the body with a link to the target repo's "How to Contribute" section, matching the wording used in that repo's existing issues:
  - parent: `Please read [how to contribute](https://github.com/aistomin/andy.grails?tab=readme-ov-file#how-to-contribute)`
  - backend: `Please read [how to contribute](https://github.com/aistomin/andy.grails.backend?tab=readme-ov-file#how-to-contribute)`
  - frontend: `Please see [how to contribute](https://github.com/aistomin/andy.grails.frontend?tab=readme-ov-file#how-to-contribute)`

---

## Code Comments

A comment records a business decision — the one thing the code cannot express: why the choice was made. Never write a comment that explains a technical detail or restates the code; if code needs a technical explanation to be readable, fix the code instead.

---

## Environment Problems

Work on the code freely: edit, build, run, test, deploy locally. The developer's environment is different: installed tools, dependencies, global settings.

If the environment gets in the way (a missing tool, a wrong version, a dependency that is not installed), stop, explain the problem, and propose the fix. Change the environment only after the owner agrees. Never work around the problem silently, and never stay silent about a fix just to avoid asking.

---

## Terminology

Phrases the owner uses as commands:

**review** — Full codebase walkthrough of the relevant repo(s). Identify issues (bugs, code smells, missing things, improvements), cross-reference with open GitHub issues, and produce a report structured as:
1. Issues already tracked in GitHub (with issue numbers)
2. Issues found in code that are NOT yet reported — candidate new tickets

Save the report to `.claude/code-review/<date>-full-review.md` in the parent repo.

**review the changes** — Review only what was modified. Run `git diff` (or `git diff master..HEAD` on a feature branch) in the relevant repo(s), inspect the changed code, and produce the same structured report limited to the scope of those changes. Do NOT walk through unrelated code.

**cleanup the local branches** — In the working copy of each of the three repos: `git checkout master && git pull && ./cleanup_branches.sh`. In the parent repo, also run `git submodule update --init --recursive` before the cleanup script.
