# SpaceX Dashboard

A full-stack dashboard for visualizing SpaceX rockets, launches, and Starlink data.

## Tech Stack

**Frontend**

* Vue 3
* TypeScript
* Vite
* D3.js
* Pinia
* Tailwind CSS

**Backend**

* Python
* FastAPI
* SpaceX API
* In-memory cache
* APScheduler

## Architecture

```text
Vue 3 / Netlify
       |
       | HTTPS
       v
FastAPI / Render
       |
       | HTTPS
       v
SpaceX API
```

The frontend communicates only with the FastAPI backend. The backend retrieves, processes, and caches data from the SpaceX API.

## Features

* Dashboard with key SpaceX metrics
* Rockets and launches visualization
* Starlink satellite visualization
* Filtering, sorting, and pagination
* Interactive D3.js charts
* API caching and scheduled data refresh
* Swagger / OpenAPI documentation

## Project Structure

```text
.
├── back-end/
│   ├── app/
│   ├── Dockerfile
│   └── pyproject.toml
│
├── front-end/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
└── netlify.toml
```

## Run Locally

### Backend

Requirements: Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
cd back-end
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

### Frontend

```bash
cd front-end
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

Set the frontend API URL in `front-end/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Docker

To run the complete application locally:

```bash
docker compose up
```

## API

| Method | Endpoint         | Description       |
| ------ | ---------------- | ----------------- |
| GET    | `/health`        | Health check      |
| GET    | `/api/dashboard` | Dashboard metrics |
| GET    | `/api/rockets`   | Rocket data       |
| GET    | `/api/launches`  | Launch data       |
| GET    | `/api/starlink`  | Starlink data     |

Swagger documentation is available at:

```text
/docs
```

## Deployment

**Frontend:** Netlify

**Backend:** Render

The frontend uses:

```env
VITE_API_BASE_URL=https://your-backend-url
```

The backend uses `CORS_ORIGINS` to allow requests from the deployed Netlify application.

## Caching

The backend uses an in-memory cache with scheduled refreshes to minimize requests to the SpaceX API.

The cache is ephemeral and is not used as a source of truth.

## Future Improvements

* Automated backend and frontend tests
* Redis for distributed caching
* CI/CD pipeline
* Application monitoring and structured logging
