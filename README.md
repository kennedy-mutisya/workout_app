# Flask Workout Application Backend

A REST API for managing workouts and reusable exercises using Flask, SQLAlchemy, Flask-Migrate, and Marshmallow.

## Requirements

- Python 3.8.13+
- Pipenv
- Git

## Installation

From the project root:

```bash
pipenv install
pipenv install --dev pytest
```

## Database setup

Run these commands from `server/` to apply the checked-in migrations and seed
the database:

```bash
pipenv run flask --app app db upgrade
pipenv run python seed.py
```

The migration environment is already checked in; do not run `db init` or
generate a migration during normal setup.

## Run the API

From `server/`:

```bash
pipenv run python app.py
```

The API runs at `http://127.0.0.1:5555`.

## Run tests

From `server/`:

```bash
pipenv run pytest -v
```

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/workouts` | List workouts |
| GET | `/workouts/<id>` | Get workout details |
| POST | `/workouts` | Create workout |
| DELETE | `/workouts/<id>` | Delete workout |
| GET | `/exercises` | List exercises |
| GET | `/exercises/<id>` | Get exercise details |
| POST | `/exercises` | Create exercise |
| DELETE | `/exercises/<id>` | Delete exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add exercise to workout |

## Validation

The application uses database constraints, SQLAlchemy model validations, and Marshmallow schema validations to protect data integrity.

## Technologies

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- pytest
