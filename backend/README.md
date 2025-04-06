# FastAPI Backend

TODO: description

## Installation
Install necessary packages using:
```bash
pip install -r requirements.txt
```

## Database

### Database Migration
This app uses `alembic` for managing database migration.

To perform migration we can use following command:
```bash
alembic upgrade head
```

### Creating New Table
1. We define the table using `sqlmodel` inside `models` directory. To create a new model, create a new file. We can use existing `models/users.py` as example.

2. Since User is a SQLModel, just make sure it’s imported in your Alembic env.py so it gets picked up for autogeneration.
    ```py
    # backend/alembic/env.py
    # ...

    # add your model's MetaData object here
    from models.users import User
    from models.yourmodel import YourModel # add this for the new model
    ```

3. Prepare the migration
    ```bash
    # Example for creating user table
    alembic revision --autogenerate -m "Add user table"
    ```

4. Run the migration
    ```bash
    # Example for creating user table
    alembic upgrade head
    ```
