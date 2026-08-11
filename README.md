# SpaceX Dashboard

A dashboard for SpaceX launch, rocket, and Starlink data: a Vue 3 frontend backed by a
FastAPI service that proxies and caches the public SpaceX API.

## 1. Project overview

- **`front-end/`** — Vue 3 + TypeScript SPA (Vite, Pinia, Vue Router, D3 charts, Tailwind).
- **`back-end/`** — FastAPI service that fetches data from the SpaceX API, caches it in
  memory, refreshes it on a schedule, and exposes it to the frontend as a small REST API.

## 2. Architecture

```
Netlify
   |
   v
Vue 3 / Vite  (static SPA, browser-side)
   |
   v  HTTPS (VITE_API_BASE_URL)
FastAPI  (containerized backend service)
   |
   v  HTTPS
SpaceX API  (api.spacexdata.com)
```

The frontend is a static site: Netlify builds it with Vite and serves the compiled
assets directly (no Node/nginx server involved). The backend is a separate, standalone
FastAPI container that the frontend calls over HTTPS. The backend is the only thing
that talks to the upstream SpaceX API — it fetches, caches, and reshapes that data
before returning it to the browser.

## 3. Local development

Requirements: Node.js 22+, Python 3.14+, [uv](https://docs.astral.sh/uv/).

**Backend**

```bash
cd back-end
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

**Frontend**

```bash
cd front-end
npm install
npm run dev
```

The frontend dev server runs at http://localhost:5173 and the backend at
http://localhost:8000 (interactive docs at http://localhost:8000/docs). By default the
backend serves mock SpaceX data (`USE_MOCK_DATA=true` in `back-end/.env`), so the app
works fully offline without hitting the real SpaceX API.

## 4. Environment variables

**Frontend** (`front-end/.env`, see [`front-end/.env.example`](front-end/.env.example)):

| Variable | Purpose | Example |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Base URL the frontend calls for all API requests | `http://localhost:8000` (dev), `https://spacex-api.yourdomain.com` (prod) |

**Backend** (`back-end/.env`, see [`back-end/.env.example`](back-end/.env.example)):

| Variable | Purpose | Default |
| --- | --- | --- |
| `USE_MOCK_DATA` | Serve canned data instead of calling the live SpaceX API | `false` |
| `SPACEX_API_BASE_URL` | Upstream SpaceX API base URL | `https://api.spacexdata.com` |
| `SPACEX_API_TIMEOUT_SECONDS` | Timeout for upstream requests | `10` |
| `CACHE_TTL_SECONDS` | How long cached responses are served before refetching | `900` |
| `CACHE_REFRESH_INTERVAL_SECONDS` | Background refresh interval | `300` |
| `CORS_ORIGINS` | Comma-separated list of origins allowed to call the API | `*` |
| `PORT` | Port the ASGI server binds to (Dockerfile) | `8000` |
| `WEB_CONCURRENCY` | Number of uvicorn worker processes (Dockerfile) | `2` |

## 5. Docker development

`docker-compose.yml` is for **local development only** — it is not used for the
Netlify deployment and isn't required to deploy the backend either.

```bash
docker compose up
```

This starts:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Swagger / OpenAPI docs: http://localhost:8000/docs

The backend container runs uvicorn with `--reload` and a bind-mounted `app/` directory
for fast iteration. The frontend container runs `npm install && npm run dev` against a
bind-mounted source tree. Neither reflects the production runtime configuration —
see sections 6 and 7 for that.

## 6. Frontend deployment (Netlify)

The frontend deploys as a static site; Netlify builds it with Vite and serves the
output directly — **no nginx, no Docker, no Node server at runtime**.

Configuration lives in [`netlify.toml`](netlify.toml) at the repo root:

- `base = "front-end"` — build runs inside `front-end/`.
- `command = "npm run build"` — standard Vite production build (`vue-tsc -b && vite build`).
- `publish = "dist"` — Vite's build output.
- A catch-all redirect (`/*` → `/index.html`, status 200) so Vue Router's history-mode
  routes (e.g. `/rockets-launches`, `/starlink`) resolve correctly on direct load or
  refresh instead of 404ing.

To deploy: connect the repo in Netlify (it will pick up `netlify.toml` automatically),
then set `VITE_API_BASE_URL` in Site settings → Environment variables to the deployed
backend's URL. No application source changes are needed to deploy.

## 7. Backend deployment

The backend ships as a standalone container ([`back-end/Dockerfile`](back-end/Dockerfile)):

- Multi-stage-free, `uv`-based install for a small, reproducible image.
- Runs as a non-root user.
- Production ASGI server: `uvicorn` with multiple workers and no `--reload`:
  ```
  uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${WEB_CONCURRENCY:-2} --proxy-headers
  ```
- All configuration (CORS, cache TTLs, upstream URL, worker count) comes from
  environment variables — nothing is hardcoded in the image.
- Exposes port `8000` and defines a `HEALTHCHECK` against `GET /health`.

Build and run:

```bash
cd back-end
docker build -t spacex-backend .
docker run -p 8000:8000 --env-file .env spacex-backend
```

Deploy the resulting image to any container host (Fly.io, Render, ECS, Cloud Run,
etc.), set the environment variables from section 4, and point the frontend's
`VITE_API_BASE_URL` at its public URL.

The backend is stateless from a business perspective: it holds no user data or
sessions, and the in-memory SpaceX cache is disposable — see section 11. It can be
restarted or horizontally scaled freely; a fresh instance just refetches from the
SpaceX API on first request.

## 8. API documentation

Interactive OpenAPI/Swagger docs are auto-generated by FastAPI and served at `/docs`
(and ReDoc at `/redoc`) on the running backend — e.g. http://localhost:8000/docs
locally.

## 9. API endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness/health check |
| `GET` | `/api/dashboard` | Aggregate dashboard stats (rockets, launches, Starlink) |
| `GET` | `/api/rockets` | List of SpaceX rockets |
| `GET` | `/api/launches` | List of SpaceX launches |
| `GET` | `/api/starlink` | List of Starlink satellites |

## 10. CORS configuration

CORS is configured via the `CORS_ORIGINS` environment variable (comma-separated list
of allowed origins), read in [`back-end/app/core/config.py`](back-end/app/core/config.py)
and applied in [`back-end/app/main.py`](back-end/app/main.py). In production this
should be set to the exact Netlify site URL(s), e.g.:

```
CORS_ORIGINS=https://your-site.netlify.app
```

Locally it defaults to allowing the Vite dev server origin (`http://localhost:5173`).
Avoid the wildcard `*` default in production.

## 11. Caching strategy

Each service (`rockets`, `launches`, `starlink`) wraps the SpaceX client with an
in-memory `TTLCache` ([`back-end/app/core/cache.py`](back-end/app/core/cache.py)).
Responses are cached for `CACHE_TTL_SECONDS` (default 15 minutes) so repeated frontend
requests don't hit the upstream SpaceX API on every call. This cache is purely
in-process and ephemeral — it is lost on restart or when scaled to multiple instances,
which is expected: it's a performance optimization, not a source of truth.

## 12. Scheduler strategy

An APScheduler `AsyncIOScheduler` background job
([`back-end/app/core/scheduler.py`](back-end/app/core/scheduler.py)) proactively
refreshes all three caches every `CACHE_REFRESH_INTERVAL_SECONDS` (default 5 minutes)
so cached data stays warm and requests rarely block on an upstream fetch. The scheduler
runs in-process, starting at app startup and shutting down at app shutdown — it is
ephemeral infrastructure state, not persisted anywhere, and each container instance
runs its own independent scheduler.

## 13. Testing

No automated test suite exists yet. To verify manually:

- Backend: `uv run uvicorn app.main:app --reload`, then check `/health` and `/docs`.
- Frontend: `npm run dev`, then exercise the Dashboard, Rockets & Launches, and
  Starlink views in a browser against the running backend.

## 14. Future improvements

- Add automated tests (pytest for the backend, Vitest/Playwright for the frontend).
- Replace the in-memory cache with a shared store (e.g. Redis) if the backend is
  scaled to multiple instances, so instances don't refetch independently.
- Add structured logging/observability for cache hit rate and upstream failures.
- Add CI to run lint/typecheck/build on every push.
