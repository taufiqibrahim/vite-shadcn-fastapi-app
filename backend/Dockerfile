FROM python:3.13-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

FROM python:3.13-slim AS final

WORKDIR /app
ENV PYTHONPATH=/app
COPY --from=builder /app/.venv .venv/

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
