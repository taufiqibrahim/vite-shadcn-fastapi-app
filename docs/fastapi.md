# FastAPI Backend

## V0 Bare Minimum

Okay, here's the bare minimum version of the framework base structure, focusing on the essential elements for API versioning, multiple auth, testing, and providing a basic structure for extension:

```
consulting_framework_base_minimal/
├── alembic/
│   ├── __init__.py
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── pyproject.toml
├── README.md
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   └── endpoints/
│   │   │       └── __init__.py
│   │   └── v2/
│   │   │   ├── __init__.py
│   │   │   └── endpoints/
│   │   │       └── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── dependencies.py
│   ├── common/
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── api/
│       ├── __init__.py
│       ├── v1/
│       │   └── __init__.py
│       └── v2/
│           └── __init__.py
├── .env
├── poetry.lock
└── LICENSE
```

## V1 Bare Minimum + Geospatial Demo

```
consulting_framework_base_minimal/
├── alembic/
│   ├── __init__.py
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── .env
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── datasets.py
│   │   │   │   └── projects.py
│   │   │   └── __init__.py
│   │   └── v2/
│   │   │   ├── __init__.py
│   │   │   └── endpoints/
│   │   │       └── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── dependencies.py
│   ├── common/
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── dataset.py
│   │   └── project.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── dataset.py
│   │   ├── geojson.py
│   │   └── project.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── dataset_service.py
│   │   └── project_service.py
├── tests/
│   ├── __init__.py
│   └── api/
│       ├── __init__.py
│       ├── v1/
│       │   ├── __init__.py
│       │   ├── test_datasets.py
│       │   └── test_projects.py
│       └── v2/
│           └── __init__.py
└── poetry.lock
```

## V3 Bare Minimum Feature-Centric + Geospatial Demo

```
consulting_framework_base_minimal/
├── alembic/
│   ├── __init__.py
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── .env
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── common/
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── datasets/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── main.py
│   ├── projects/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── services.py
├── tests/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── test_datasets.py
│   │   │   ├── test_projects.py
│   │   │   └── test_users.py
│   │   └── v2/
│   │       └── __init__.py
└── poetry.lock
```