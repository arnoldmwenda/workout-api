# Workout Tracker API

A simple REST API for personal trainers to track workouts and the exercises
performed in each one. Built with Flask, Flask-SQLAlchemy, Flask-Migrate,
and Marshmallow.

## Features

- Create, view, and delete **workouts**
- Create, view, and delete **exercises**
- Link exercises to workouts through a **join table** (`workout_exercises`)
  that stores reps, sets, and duration for that specific exercise in that
  specific workout
- Input validation at three levels: database constraints, model validations
  (`@validates`), and Marshmallow schema validation
- JSON error responses with appropriate HTTP status codes

## Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate (Alembic)
- Marshmallow
- SQLite

## Project Structure

```
workout-api/
│
├── Pipfile
├── README.md
├── .gitignore
│
└── server/
    ├── app.py          # Flask app + routes
    ├── models.py       # SQLAlchemy models
    ├── schemas.py       # Marshmallow schemas
    ├── seed.py         # Sample data
    ├── app.db          # SQLite database (created after migration)
    └── migrations/      # Flask-Migrate files
```

## Installation

1. Clone the repo and move into it:

   ```bash
   cd workout-api
   ```

2. Install dependencies with Pipenv:

   ```bash
   pipenv install
   pipenv shell
   ```

   (Or, if you're not using Pipenv, install the packages listed in the
   `Pipfile` with `pip` instead.)

## Creating the Database

From inside the `server/` folder, run the migration commands:

```bash
cd server
export FLASK_APP=app.py     # on Windows (cmd): set FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

This creates `app.db` with three tables: `workouts`, `exercises`, and
`workout_exercises`.

## Seeding the Database

Still inside `server/`, run:

```bash
python seed.py
```

This clears any existing data and adds a handful of sample exercises,
workouts, and workout_exercises so you have something to test against.

## Running the Server

```bash
python app.py
```

The API will start at `http://127.0.0.1:5555`.

## Endpoints

### Workouts

| Method | Route              | Description                              |
|--------|---------------------|-------------------------------------------|
| GET    | `/workouts`         | Get all workouts                          |
| GET    | `/workouts/<id>`    | Get one workout, with its exercises       |
| POST   | `/workouts`         | Create a new workout                      |
| DELETE | `/workouts/<id>`    | Delete a workout (and its workout_exercise rows) |

**POST /workouts body:**

```json
{
  "date": "2026-07-10",
  "duration_minutes": 40,
  "notes": "Leg day"
}
```

### Exercises

| Method | Route               | Description                              |
|--------|----------------------|-------------------------------------------|
| GET    | `/exercises`         | Get all exercises                         |
| GET    | `/exercises/<id>`    | Get one exercise, with the workouts that use it |
| POST   | `/exercises`         | Create a new exercise                     |
| DELETE | `/exercises/<id>`    | Delete an exercise (and its workout_exercise rows) |

**POST /exercises body:**

```json
{
  "name": "Deadlift",
  "category": "Strength",
  "equipment_needed": true
}
```

### Workout Exercises (join table)

| Method | Route                                                              | Description                        |
|--------|----------------------------------------------------------------------|-------------------------------------|
| POST   | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout        |

**POST body:**

```json
{
  "reps": 10,
  "sets": 3,
  "duration_seconds": null
}
```

## Validation

- **Database constraints:** exercise `name`, workout `date`, and workout
  `duration_minutes` cannot be `NULL`.
- **Model validations** (`@validates`): exercise name can't be blank, workout
  duration must be greater than 0, and reps/sets/duration_seconds can't be
  negative.
- **Schema validations** (Marshmallow): required fields, minimum lengths, and
  numeric ranges are checked before the data ever reaches the database.

## Error Responses

Errors are always returned as JSON, e.g.:

```json
{ "error": "Workout not found" }
```

or, for validation errors:

```json
{ "error": { "duration_minutes": ["Duration must be positive."] } }
```

| Status | Meaning                          |
|--------|------------------------------------|
| 200    | OK                                  |
| 201    | Created                            |
| 400    | Bad Request (validation error)      |
| 404    | Not Found                          |
