import os
import sys
import unittest

# Make the server directory available for imports.
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

from app import app
from models import db, Workout, Exercise, WorkoutExercise


class TestWorkoutApp(unittest.TestCase):
    def setUp(self):
        # Push an application context before accessing SQLAlchemy.
        self.app_context = app.app_context()
        self.app_context.push()

        app.config["TESTING"] = True
        self.client = app.test_client()

        # Create a clean database for each test.
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_workout(self):
        """Create a workout through the API."""
        return self.client.post(
            "/workouts",
            json={
                "date": "2026-10-20",
                "duration_minutes": 45,
                "notes": "Morning workout",
            },
        )

    def create_exercise(self, name="Squats"):
        """Create an exercise through the API."""
        return self.client.post(
            "/exercises",
            json={
                "name": name,
                "category": "Strength",
                "equipment_needed": False,
            },
        )

    # ---------------- HOME ROUTE ----------------

    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_route_returns_json(self):
        response = self.client.get("/")
        self.assertTrue(response.is_json)
        self.assertIn("message", response.get_json())

    # ---------------- WORKOUT ROUTES ----------------

    def test_create_workout(self):
        response = self.create_workout()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["duration_minutes"], 45)

    def test_create_workout_requires_fields(self):
        response = self.client.post(
            "/workouts",
            json={"notes": "Missing required fields"},
        )

        self.assertEqual(response.status_code, 400)

    def test_reject_negative_workout_duration(self):
        response = self.client.post(
            "/workouts",
            json={
                "date": "2026-10-20",
                "duration_minutes": -10,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_list_workouts(self):
        self.create_workout()

        response = self.client.get("/workouts")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_single_workout(self):
        created = self.create_workout()
        workout_id = created.get_json()["id"]

        response = self.client.get(f"/workouts/{workout_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], workout_id)

    def test_missing_workout_returns_404(self):
        response = self.client.get("/workouts/9999")

        self.assertEqual(response.status_code, 404)

    def test_delete_workout(self):
        created = self.create_workout()
        workout_id = created.get_json()["id"]

        response = self.client.delete(f"/workouts/{workout_id}")

        self.assertEqual(response.status_code, 204)

        missing = self.client.get(f"/workouts/{workout_id}")
        self.assertEqual(missing.status_code, 404)

    # ---------------- EXERCISE ROUTES ----------------

    def test_create_exercise(self):
        response = self.create_exercise()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Squats")

    def test_reject_blank_exercise_name(self):
        response = self.client.post(
            "/exercises",
            json={
                "name": "   ",
                "category": "Strength",
                "equipment_needed": False,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_reject_blank_exercise_category(self):
        response = self.client.post(
            "/exercises",
            json={
                "name": "Squats",
                "category": "   ",
                "equipment_needed": False,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_reject_duplicate_exercise_name(self):
        self.create_exercise()

        response = self.create_exercise()

        self.assertEqual(response.status_code, 400)

    def test_list_exercises(self):
        self.create_exercise()

        response = self.client.get("/exercises")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_single_exercise(self):
        created = self.create_exercise()
        exercise_id = created.get_json()["id"]

        response = self.client.get(f"/exercises/{exercise_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], exercise_id)

    def test_missing_exercise_returns_404(self):
        response = self.client.get("/exercises/9999")

        self.assertEqual(response.status_code, 404)

    def test_delete_exercise(self):
        created = self.create_exercise()
        exercise_id = created.get_json()["id"]

        response = self.client.delete(f"/exercises/{exercise_id}")

        self.assertEqual(response.status_code, 204)

        missing = self.client.get(f"/exercises/{exercise_id}")
        self.assertEqual(missing.status_code, 404)

    # ---------------- WORKOUT-EXERCISE RELATIONSHIPS ----------------

    def test_add_exercise_to_workout(self):
        workout = self.create_workout().get_json()
        exercise = self.create_exercise().get_json()

        response = self.client.post(
            f"/workouts/{workout['id']}/exercises/"
            f"{exercise['id']}/workout_exercises",
            json={"reps": 12, "sets": 3},
        )

        self.assertEqual(response.status_code, 201)

    def test_reject_duplicate_workout_exercise(self):
        workout = self.create_workout().get_json()
        exercise = self.create_exercise().get_json()

        url = (
            f"/workouts/{workout['id']}/exercises/"
            f"{exercise['id']}/workout_exercises"
        )

        first = self.client.post(url, json={"reps": 12, "sets": 3})
        second = self.client.post(url, json={"reps": 10, "sets": 2})

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 400)

    def test_reject_invalid_reps(self):
        workout = self.create_workout().get_json()
        exercise = self.create_exercise().get_json()

        response = self.client.post(
            f"/workouts/{workout['id']}/exercises/"
            f"{exercise['id']}/workout_exercises",
            json={"reps": 0, "sets": 3},
        )

        self.assertEqual(response.status_code, 400)

    def test_workout_includes_exercises_and_metrics(self):
        workout = self.create_workout().get_json()
        exercise = self.create_exercise().get_json()

        self.client.post(
            f"/workouts/{workout['id']}/exercises/"
            f"{exercise['id']}/workout_exercises",
            json={"reps": 12, "sets": 3},
        )

        response = self.client.get(f"/workouts/{workout['id']}")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("workout_exercises", data)
        self.assertEqual(len(data["workout_exercises"]), 1)
        self.assertEqual(data["workout_exercises"][0]["reps"], 12)
        self.assertEqual(data["workout_exercises"][0]["sets"], 3)

    def test_exercise_includes_associated_workouts(self):
        workout = self.create_workout().get_json()
        exercise = self.create_exercise().get_json()

        self.client.post(
            f"/workouts/{workout['id']}/exercises/"
            f"{exercise['id']}/workout_exercises",
            json={"reps": 12, "sets": 3},
        )

        response = self.client.get(f"/exercises/{exercise['id']}")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("workout_exercises", data)
        self.assertEqual(len(data["workout_exercises"]), 1)

    def test_deleting_workout_removes_associations(self):
        workout = self.create_workout().get_json()
        exercise = self.create_exercise().get_json()

        self.client.post(
            f"/workouts/{workout['id']}/exercises/"
            f"{exercise['id']}/workout_exercises",
            json={"reps": 12, "sets": 3},
        )

        response = self.client.delete(f"/workouts/{workout['id']}")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(WorkoutExercise.query.count(), 0)

    def test_deleting_exercise_removes_associations(self):
        workout = self.create_workout().get_json()
        exercise = self.create_exercise().get_json()

        self.client.post(
            f"/workouts/{workout['id']}/exercises/"
            f"{exercise['id']}/workout_exercises",
            json={"reps": 12, "sets": 3},
        )

        response = self.client.delete(f"/exercises/{exercise['id']}")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(WorkoutExercise.query.count(), 0)


if __name__ == "__main__":
    unittest.main()
