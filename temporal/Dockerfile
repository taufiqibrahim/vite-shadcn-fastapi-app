FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install Linux dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    postgresql-client \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install poetry and Python dependencies
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Copy workflow code
COPY . /app/

CMD ["poetry", "run", "python", "-m", "geospatial_mapping_app.worker"]
