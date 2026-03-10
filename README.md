# FlowSync Pipeline

A containerized data pipeline with three Docker services:

- **Flask Mock Server** – Serves customer data from JSON on port 5000
- **FastAPI Pipeline Service** – Ingests and exposes customer data via port 8000
- **PostgreSQL** – Persistent storage on port 5432

## Architecture

```
Flask (JSON source) → FastAPI (ingest + upsert) → PostgreSQL → API response
```

## Prerequisites

- Docker Desktop (running)
- `docker-compose` v2+

## Quick Start

```bash
# Clone and enter the project
git clone <repo-url>
cd flowsync-pipeline

# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

## API Endpoints

### Flask Mock Server (port 5000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/customers?page=1&limit=10` | Paginated customer list |
| GET | `/api/customers/{id}` | Single customer by ID |

### FastAPI Pipeline Service (port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/ingest` | Fetch from Flask → upsert to DB |
| GET | `/api/customers?page=1&limit=10` | Paginated from database |
| GET | `/api/customers/{id}` | Single customer from database |
| GET | `/docs` | Swagger UI |

## Testing

```bash
# Health checks
curl http://localhost:5000/api/health
curl http://localhost:8000/api/health

# Flask – list customers (paginated)
curl "http://localhost:5000/api/customers?page=1&limit=5"

# Flask – single customer
curl http://localhost:5000/api/customers/CUST-001

# Ingest all data from Flask into PostgreSQL
curl -X POST http://localhost:8000/api/ingest

# Query customers from database
curl "http://localhost:8000/api/customers?page=1&limit=5"

# Single customer from database
curl http://localhost:8000/api/customers/CUST-001
```

## Project Structure

```
flowsync-pipeline/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/
│   │   └── customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── database.py
    ├── models/
    │   └── customer.py
    ├── services/
    │   └── ingestion.py
    ├── Dockerfile
    └── requirements.txt
```

## Stopping Services

```bash
docker-compose down          # stop containers
docker-compose down -v       # stop + remove volumes (clears DB)
```
