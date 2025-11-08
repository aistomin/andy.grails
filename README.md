# Andy Grails' Website

This is the main repository for the [Andy Grails' website](https://andy-grails.de/)
— a personal project to showcase and stream music under the nickname _Andy Grails_.
The site is powered by a **Java backend** and an **Angular frontend**, structured
as Git submodules.

## Repository Structure

This repository acts as a wrapper for the two core components:

andy.grails/

- andy.grails.backend/ (Java Spring Boot backend: API, data services)
- andy.grails.frontend/ (Angular frontend: UI and client logic)

### Submodules

- [**backend**](https://github.com/aistomin/andy.grails.backend):  
  A Java Spring Boot application providing RESTful APIs to serve music data,
  media, and metadata.

- [**frontend**](https://github.com/aistomin/andy.grails.frontend):  
  An Angular-based web application that presents the user interface, consumes
  the backend API, and delivers the overall user experience.

## Getting Started

To clone this repository:

```bash
git clone git@github.com:aistomin/andy.grails.git
```

**Note:** Submodules are not required to be initialized for running the application with Docker. The scripts pull Docker images directly from Docker Hub based on Git revisions.

Each submodule has its own `README.md` with specific instructions for building
and running the backend and frontend.

## Quick Start with Docker

This repository includes convenient scripts to run the entire application stack using Docker:

### Prerequisites

- Docker and Docker Compose installed
- Git repository cloned (submodules are **not** required to be initialized)

### Available Scripts

#### 🚀 `start.sh` - Start the Application

Starts the complete application stack (frontend + backend + database) using Docker Compose.

```bash
./start.sh
```

**What it does:**

- Gets the current Git revision from the main repository
- Pulls Docker images from Docker Hub using revision-based tags
- Starts PostgreSQL database, backend API, and frontend
- Provides access URLs for all services

**Access URLs:**

- Frontend: http://localhost:4200
- Backend API: http://localhost:8080
- Database: localhost:55432

#### 🛑 `stop.sh` - Stop the Application

Stops all running containers and cleans up the application stack.

```bash
./stop.sh
```

#### 🚀 `deploy.sh` - Deploy to Specific Revision

Deploys the application to a specific Git revision, allowing easy rollbacks and deployments.

```bash
./deploy.sh <git-revision>
```

**Examples:**

```bash
# Deploy to a specific commit
./deploy.sh abc1234

# Deploy to a branch
./deploy.sh main

# Deploy to a tag
./deploy.sh v1.0.0
```

**What it does:**

1. Checks for local changes (fails if any uncommitted changes exist)
2. Validates the specified Git revision exists
3. Checks out the revision and updates submodules
4. Stops the current application
5. Starts the application with the new revision

**Safety Features:**

- Prevents deployment with uncommitted changes
- Validates revision existence before checkout
- Provides helpful error messages and suggestions

### Docker Images

The application uses Docker Hub images with revision-based tagging:

- **Backend**: `andygrails/andy-grails-backend:<revision>`
- **Frontend**: `andygrails/andy-grails-frontend:<revision>`

### Environment Variables

You can customize the database configuration using environment variables:

- `DB_NAME` (default: andy_grails)
- `DB_USER` (default: andy)
- `DB_PASSWORD` (default: andy)

### Useful Commands

```bash
# View application logs
docker compose logs -f

# View logs for specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db

# Remove all containers and volumes
docker compose down -v

# Rebuild and start (if you need to rebuild images)
docker compose up --build -d
```

## Playwright End-to-End Tests

E2E tests live in this repository (outside the submodules) under `playwright/` and assume the application is already running in Docker.

### Prerequisites

- Run the application stack and ensure the frontend is reachable at `http://localhost:4200`:

  ```bash
  ./start.sh
  ```

### Running the Tests

```bash
cd playwright
npm install          # only needed once
npx playwright install  # downloads the required browsers (first time only)
npm test             # runs Playwright against http://localhost:4200
```

To target a different URL, override the `PLAYWRIGHT_BASE_URL` environment variable:

```bash
PLAYWRIGHT_BASE_URL=http://localhost:4300 npm test
```
