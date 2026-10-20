# Flask Workout Application Backend

A REST API for managing workouts and reusable exercises using Flask, SQLAlchemy, Flask-Migrate, and Marshmallow.

## Features

- Create, view, and delete workouts.
- Create, view, and delete exercises.
- Associate exercises with workouts.
- Store sets, reps, and duration for each workout exercise.
- Validate incoming data and enforce database constraints.

## Requirements

- Python 3.8.13 or later
- Pipenv
- Git

## Installation

```bash
pipenv install
pipenv install --dev pytest
```

## Run the application

From the project root:

```bash
pipenv run python server/app.py
```

The API runs at `http://127.0.0.1:5555`.

## Run tests

```bash
pipenv run pytest -v
```

## Database migrations

Run these commands from the project root after configuring the application:

```bash
pipenv run flask --app server/app.py db init
pipenv run flask --app server/app.py db migrate -m "Create workout tables"
pipenv run flask --app server/app.py db upgrade
```

## API endpoints

| Method | Endpoint |
|---|---|
| GET | `/` |
| GET | `/workouts` |
| GET | `/workouts/<id>` |
| POST | `/workouts` |
| DELETE | `/workouts/<id>` |
| GET | `/exercises` |
| GET | `/exercises/<id>` |
| POST | `/exercises` |
| DELETE | `/exercises/<id>` |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` |

The workout and exercise endpoints will be implemented in subsequent development steps.
