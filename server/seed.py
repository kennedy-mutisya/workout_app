from datetime import date, timedelta

from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():
    db.drop_all()
    db.create_all()

    workout1 = Workout(
        date=date.today(), duration_minutes=45, notes="Full body strength training"
    )

    workout2 = Workout(
        date=date.today() + timedelta(days=1),
        duration_minutes=30,
        notes="Cardio session",
    )

    workout3 = Workout(
        date=date.today() + timedelta(days=2), duration_minutes=60, notes="Leg day"
    )

    squat = Exercise(name="Squats", category="Strength", equipment_needed=False)

    push_up = Exercise(name="Push-ups", category="Strength", equipment_needed=False)

    treadmill = Exercise(
        name="Treadmill Running", category="Cardio", equipment_needed=True
    )

    plank = Exercise(name="Plank", category="Core", equipment_needed=False)

    db.session.add_all([workout1, workout2, workout3, squat, push_up, treadmill, plank])
    db.session.flush()

    db.session.add_all(
        [
            WorkoutExercise(workout=workout1, exercise=squat, sets=3, reps=12),
            WorkoutExercise(workout=workout1, exercise=push_up, sets=3, reps=10),
            WorkoutExercise(
                workout=workout2, exercise=treadmill, duration_seconds=1200
            ),
            WorkoutExercise(workout=workout3, exercise=squat, sets=4, reps=10),
            WorkoutExercise(
                workout=workout3, exercise=plank, sets=3, duration_seconds=60
            ),
        ]
    )

    db.session.commit()

    print("Database seeded successfully.")
    print(f"Workouts: {Workout.query.count()}")
    print(f"Exercises: {Exercise.query.count()}")
    print(f"Workout exercises: {WorkoutExercise.query.count()}")
