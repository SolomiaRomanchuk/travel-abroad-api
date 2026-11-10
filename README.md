# Travel Abroad API

FastAPI backend for managing international travel visits.

## Technologies
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- httpx
- asyncio
- Docker 
- Alembic


## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
fastapi dev app/main.py
```

Documentation: http://127.0.0.1:8000/docs

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /visits | List visits with filters and pagination |
| GET | /visits/{visit_id} | Get visit by ID |
| POST | /visits | Create a visit |
| PATCH | /visits/{visit_id} | Update a visit |
| DELETE | /visits/{visit_id} | Delete a visit |
| GET | /explore | Get weather and currency exchange rate |

## Features

- CRUD operations
- Data validation
- SQLite database
- Country filtering and pagination
- Concurrent external API requests

## API Documentation

Add a screenshot of the Swagger UI here.

## Docker and PostgreSQL

Start the application:

```bash
docker compose up --build -d
```

Create the initial migration:

```bash
docker compose exec api alembic revision --autogenerate -m "initial migration"
```

Apply migrations:

```bash
docker compose exec api alembic upgrade head
```

API documentation:
http://127.0.0.1:8000/docs

## Additional endpoints

- POST /visits/{visit_id}/expenses
- GET /visits/{visit_id}/expenses

## Database

The project uses PostgreSQL 17, SQLAlchemy ORM,
ForeignKey relationships and Alembic migrations.
