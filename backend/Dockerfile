FROM python:3.13-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Copy migration code
COPY alembic.ini /app/
COPY alembic /app/alembic

# Copy source code
COPY src /app/src

# Ensure the startup script is executable
RUN chmod +x /app/src/scripts/startup.sh

# Set the entrypoint to the startup script
ENTRYPOINT ["/app/src/scripts/startup.sh"]

EXPOSE 8000
