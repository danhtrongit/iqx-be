# IQX Backend

Backend API for the IQX application with PostgreSQL/TimescaleDB integration.

## PostgreSQL/TimescaleDB Setup

### Prerequisites

- PostgreSQL 12+ with TimescaleDB extension installed
- Python 3.9+

### Database Setup

1. Install TimescaleDB (if not already installed):

```bash
# For Docker
docker run -d --name timescaledb \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=iqx \
  timescale/timescaledb:latest-pg14
```

2. Create a database and enable the TimescaleDB extension:

```sql
CREATE DATABASE iqx;
\c iqx
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
```

3. Create a `.env` file in the project root with the following content (adjust values as needed):

```
# API Configuration
PROJECT_NAME=IQX API
API_V1_STR=/api/v1

# PostgreSQL/TimescaleDB Connection
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=iqx
POSTGRES_PORT=5432
POSTGRES_SCHEMA=public

# TimescaleDB Configuration
TIMESCALEDB_ENABLED=true

# CORS Configuration
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Setup and Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Initialize the database (create tables):

```bash
# Initialize Alembic
alembic init alembic

# Edit alembic.ini and set the sqlalchemy.url
# Edit alembic/env.py to import Base from app.core.database and models

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

3. Run the application:

```bash
uvicorn app.main:app --reload
```

4. Access the API documentation at http://localhost:8000/docs

## TimescaleDB Features Used

This application demonstrates the following TimescaleDB features:

1. **Hypertables**: The `sensor_data` table is converted to a TimescaleDB hypertable for efficient time-series data storage.

2. **Automatic Data Compression**: Data older than 30 days is automatically compressed to save storage space.

3. **Continuous Aggregates**: Pre-calculated aggregations for faster query performance on historical data.

## Project Structure

```
backend/
  ├── alembic/                 # Database migrations
  ├── app/
  │   ├── api/                 # API endpoints
  │   ├── core/                # Core application components
  │   │   ├── config.py        # Application configuration
  │   │   ├── database.py      # Database connection
  │   │   ├── dependencies.py  # FastAPI dependencies
  │   │   └── timescale_utils.py  # TimescaleDB utilities
  │   ├── crud/                # CRUD operations
  │   ├── models/              # SQLAlchemy models
  │   ├── schemas/             # Pydantic schemas
  │   ├── services/            # Business logic
  │   └── utils/               # Utility functions
  ├── .env                     # Environment variables (create from examples)
  └── requirements.txt         # Python dependencies
```
# iqx-be
