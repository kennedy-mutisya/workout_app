from datetime import date

from app import app
from models import db, Workout, Exercise, WorkoutExercise


def seed_database():
    """Create sample workout data without duplicating existing records."""
    with app.app_context():
        workouts_data = [
            {
                "date": date(2026, 10, 20),
                "duration_minutes": 45,
                "notes": "Morning strength training",
            },
            {
                "date": date(2026, 10, 21),
                "duration_minutes": 30,
                "notes": "Cardio session",
            },
            {
                "date": date(2026, 10, 22),
                "duration_minutes": 60,
                "notes": "Full body workout",
            },
        ]

        exercises_data = [
            {
                "name": "Squats",
                "category": "Strength",
                "equipment_needed": False,
            },
            {
                "name": "Push-ups",
                "category": "Strength",
                "equipment_needed": False,
            },
            {
                "name": "Treadmill Running",
                "category": "Cardio",
                "equipment_needed": True,
            },
            {
                "name": "Plank",
                "category": "Core",
                "equipment_needed": False,
            },
        ]

        # Create workouts only if their identifying details do not exist.
        workouts = []
        for data in workouts_data:
            workout = Workout.query.filter_by(
                date=data["date"],
                notes=data["notes"],
            ).first()

            if workout is None:
                workout = Workout(**data)
                db.session.add(workout)

            workouts.append(workout)

        # Create exercises only if their unique names do not exist.
        exercises = []
        for data in exercises_data:
            exercise = Exercise.query.filter_by(name=data["name"]).first()

            if exercise is None:
                exercise = Exercise(**data)
                db.session.add(exercise)

            exercises.append(exercise)

        # Persist new workouts and exercises before creating associations.
        db.session.flush()

        # Add each workout-exercise association only once.
        associations = [
            (0, 0, 12, 3),
            (0, 1, 10, 3),
            (1, 2, None, None),
            (2, 0, 15, 4),
            (2, 3, None, 3),
        ]

        for workout_index, exercise_index, reps, sets in associations:
            workout = workouts[workout_index]
            exercise = exercises[exercise_index]

            existing = WorkoutExercise.query.filter_by(
                workout_id=workout.id,
                exercise_id=exercise.id,
            ).first()

            if existing is None:
                db.session.add(
                    WorkoutExercise(
                        workout_id=workout.id,
                        exercise_id=exercise.id,
                        reps=reps,
                        sets=sets,
                    )
                )

        db.session.commit()

        print("Database seeded successfully.")
        print(f"Workouts: {Workout.query.count()}")
        print(f"Exercises: {Exercise.query.count()}")
        print(f"Workout-exercise associations: {WorkoutExercise.query.count()}")


if __name__ == "__main__":
    try:
        seed_database()
    except Exception:
        with app.app_context():
            db.session.rollback()
        raise
