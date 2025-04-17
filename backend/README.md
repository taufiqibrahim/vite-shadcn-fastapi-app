# FastAPI Backend

TODO: description

## Quickstart
```bash
cd backend
poetry install
fastapi dev src/main.py
```

## Installation
Install necessary packages using:
```bash
pip install poetry
poetry install
```

## Environment Variables
Create `backend/.env` based on `backend/.env.example` and update accordingly.

## Database

### Database Migration
This app uses `alembic` for managing database migration.

To perform migration we can use following command:
```bash
alembic upgrade head
```

### Creating New Table
We will show how we initiate the first migration as example.

1. We define the table using `sqlmodel` inside `models` directory. To create a new model, create a new file. We can use existing `backend/src/auth/models.py` as example.

2. Register the model files in the Alembic's `env.py` so it gets picked up for autogeneration.
    ```py
    # backend/alembic/env.py
    # ...

    # add your model's MetaData object here
    from src.auth.models import Account, APIKey, UserProfile  # noqa
    # from models.yourmodel import YourModel # add this for the new model
    ```

3. Prepare the migration
    ```bash
    # Example for creating auth tables
    alembic revision --autogenerate -m "add initial tables" --rev-id 001
    ```

4. Run the migration
    ```bash
    # Example for creating user table
    alembic upgrade head
    ```

## Load Demo Data
This repository provides demo data which can be invoked using following command:
```bash
# make sure in backend directory
cd backend

poetry run python src/scripts/load_demo_data.py
```