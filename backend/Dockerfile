FROM python:3.13 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

FROM python:3.13-slim

WORKDIR /app
ENV PYTHONPATH=/app/backend
COPY --from=builder /app/.venv .venv/
COPY backend /app/backend
EXPOSE 8000
# CMD ["/app/.venv/bin/fastapi", "run"]
CMD ["/app/.venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
