from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


def error_response(message, status_code):
    return make_response(jsonify({"errors": [message]}), status_code)


@app.route("/", methods=["GET"])
def index():
    return (
        jsonify({"message": "Workout Application API is running", "status": "success"}),
        200,
    )


# WORKOUT ROUTES


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return error_response("Workout not found.", 404)

    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response("Request body must be a JSON object.", 400)

    try:
        validated_data = workout_schema.load(data)
        workout = Workout(**validated_data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except (ValueError, TypeError) as error:
        db.session.rollback()
        return error_response(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response("Invalid workout data.", 400)


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return error_response("Workout not found.", 404)

    db.session.delete(workout)
    db.session.commit()

    return "", 204


# EXERCISE ROUTES


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return error_response("Exercise not found.", 404)

    return jsonify(exercise_schema.dump(exercise)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response("Request body must be a JSON object.", 400)

    try:
        validated_data = exercise_schema.load(data)
        exercise = Exercise(**validated_data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except (ValueError, TypeError) as error:
        db.session.rollback()
        return error_response(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response(
            "Exercise name already exists or data violates a constraint.", 400
        )


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return error_response("Exercise not found.", 404)

    db.session.delete(exercise)
    db.session.commit()

    return "", 204


# WORKOUT-EXERCISE ROUTE


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return error_response("Workout not found.", 404)

    if exercise is None:
        return error_response("Exercise not found.", 404)

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response("Request body must be a JSON object.", 400)

    try:
        validated_data = workout_exercise_schema.load(data)

        association = WorkoutExercise(
            workout_id=workout_id, exercise_id=exercise_id, **validated_data
        )

        db.session.add(association)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": association.id,
                    "workout_id": association.workout_id,
                    "exercise_id": association.exercise_id,
                    "reps": association.reps,
                    "sets": association.sets,
                    "duration_seconds": association.duration_seconds,
                    "exercise": {
                        "id": exercise.id,
                        "name": exercise.name,
                        "category": exercise.category,
                        "equipment_needed": exercise.equipment_needed,
                    },
                }
            ),
            201,
        )

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except (ValueError, TypeError) as error:
        db.session.rollback()
        return error_response(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response(
            "This exercise is already in the workout or the data is invalid.", 400
        )


if __name__ == "__main__":
    app.run(port=5555, debug=True)
