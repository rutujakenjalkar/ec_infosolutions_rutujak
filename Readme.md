

```markdown
# Music Discovery API

A production-grade RESTful API built with Django, Django REST Framework, Celery, Redis, PostgreSQL, and Nginx. The application provides music recommendation tracking, user activity analytics, and asynchronous background tasks.

---

## Candidate Submission Details

* **Current / Last Drawn CTC:** [NA]
* **Notice Period:** [Immediate / 15 Days]
* **Current Location:** Baner Pune, India
* **Willingness to work from Baner office:** Yes

---

## Features

* **User Profiles & Activity Tracking:** Full CRUD endpoints for managing user profiles, favorite genres, and logging activity data.
* **Asynchronous Recommendations:** Background recalculations for recommendations powered by Celery workers and Redis.
* **Analytics Engine:** Summary and trend analytics utilizing Django aggregation queries (`Count`, `Q`).
* **Caching Layer:** Redis integration for response caching and fast retrieval.
* **Production Stack:** Fully containerized setup with Docker, Docker Compose, and Nginx reverse proxy.

---

## Tech Stack

* **Framework:** Python 3.10+, Django, Django REST Framework
* **Database:** PostgreSQL
* **Task Queue & Caching:** Celery, Redis
* **Web Server:** Nginx
* **Containerization:** Docker, Docker Compose

---

## Getting Started

### Prerequisites

* [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

---

## Running the Application

### 1. One-Command Setup

To build images, start containers, and apply database migrations automatically:

```bash
make setup

```

Or using Docker Compose directly:

```bash
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate

```

The API will be accessible at `http://localhost:8000/`.

---

### 2. Management Commands

| Action | Makefile Shortcut | Direct Command |
| --- | --- | --- |
| **Start Containers** | `make up` | `docker-compose up -d` |
| **Stop Containers** | `make down` | `docker-compose down` |
| **Apply Migrations** | `make migrate` | `docker-compose exec web python manage.py migrate` |
| **Create Migrations** | `make makemigrations` | `docker-compose exec web python manage.py makemigrations` |
| **Run Unit Tests** | `make test` | `docker-compose exec web python manage.py test` |
| **View Live Logs** | `make logs` | `docker-compose logs -f` |
| **Access Shell** | `make shell` | `docker-compose exec web python manage.py shell` |
| **Full Reset** | `make clean` | `docker-compose down -v` |

---

## Running Tests

The test suite includes 14 unit and integration tests covering API views, serializers, authentication, and asynchronous tasks.

Execute the tests inside the web container:

```bash
make test

```

Or directly via Docker Compose:

```bash
docker-compose exec web python manage.py test

```

---

## API Endpoints Overview

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` / `POST` | `/api/profiles/` | List or create user profiles |
| `GET` / `POST` | `/api/activities/` | Retrieve or log user playback activities |
| `GET` | `/api/recommendations/` | Retrieve cached user recommendations |
| `POST` | `/api/recommendations/refresh/` | Trigger asynchronous recommendation recalculation |
| `GET` | `/api/analytics/summary/` | Get overall application metrics and user counts |
| `GET` | `/api/analytics/trends/` | Get top active users and listening trend analytics |

---


```

```