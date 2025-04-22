#!/bin/bash

# Ensure the virtual environment is activated
echo "Activating virtual environment..."
source /app/.venv/bin/activate

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Run any custom Python script (e.g., database seeding)
echo "Running load demo data script..."
python src/scripts/load_demo_data.py

# Start the FastAPI app
echo "Starting FastAPI app..."
uvicorn src.main:app --host 0.0.0.0 --port 8000
