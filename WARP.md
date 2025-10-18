# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Common Commands

### Running the Application
```bash
# Start the FastAPI server
python app/app.py
# or
uvicorn app.app:app --reload
```

### Testing
```bash
# Run pytest (pytest is in requirements.txt)
pytest
```

### Dependencies
```bash
# Install dependencies
pip install -r requirements.txt
```

## Architecture Overview

This is a **FastAPI-based Finance Tracker** application with a clean layered architecture:

### Core Architecture Pattern
The application follows a **3-layer architecture**:
- **APIs** (`app/apis/`) - FastAPI routers handling HTTP endpoints
- **Services** (`app/services/`) - Business logic layer with validation and orchestration
- **Repositories** (`app/repositories/`) - Data access layer with direct database operations

### Database & Models
- **Database**: PostgreSQL with psycopg2
- **Models** (`app/models/`) - Pydantic models for request/response validation
- **Connection**: Uses environment variables (`DATABASE_URL`) via python-dotenv
- **Pattern**: Raw SQL queries with RealDictCursor for JSON-like results

### Key Domain Entities
- **Users** - User management and authentication (Argon2 password hashing)
- **Banks** - Bank information and configurations
- **Accounts** - User bank accounts
- **Transactions** - Financial transactions (core entity)
- **Categories/Tags** - Transaction categorization and tagging
- **Tag Rules** - Automated transaction categorization rules
- **Category Targets** - Budgeting/spending targets

### File Structure Pattern
Each domain entity follows the same structure:
```
{entity}/
├── models/{entity}.py          # Pydantic models (base + upsert variants)
├── repositories/{entity}_repository.py  # Database operations
├── services/{entity}_service.py         # Business logic
└── apis/{entity}.py            # FastAPI endpoints
```

## Development Guidelines

### Repository Layer
- All repository functions handle their own database connections
- Use `RealDictCursor` for SELECT operations to get dict-like results
- Always include proper connection cleanup in try/finally blocks
- Return `Optional[Model]` for single entities, `List[Model]` for collections

### Service Layer
- Validates input parameters (e.g., checking for positive IDs)
- Orchestrates repository calls and business logic
- Handles data transformation between repository and API layers
- Uses centralized logging via `utils.logger`

### API Layer
- Uses FastAPI with automatic OpenAPI documentation
- Follows RESTful conventions with appropriate HTTP status codes
- Returns Pydantic models for type safety
- Includes proper error handling with HTTPException

### Environment Setup
- Requires `.env` file with `DATABASE_URL` (and optionally `TEST_DATABASE_URL`)
- Uses `python-dotenv` for environment variable loading
- Centralized database connection in `db/database.py`

### Logging
- Centralized logging system in `utils/logger.py` with rotating file handler
- Logs to both console and files in `logs/` directory
- Repository and service layers include comprehensive error logging

### Security
- Password hashing uses Argon2 (`utils/security.py`)
- CORS middleware configured for cross-origin requests