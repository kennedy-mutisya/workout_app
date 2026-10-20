"""Repair databases stamped before workout tables were created.

Revision ID: b7f6c9a1d204
Revises: 217bde5e2b3d
Create Date: 2026-10-20 14:20:00

"""
from alembic import op
import sqlalchemy as sa


revision = "b7f6c9a1d204"
down_revision = "217bde5e2b3d"
branch_labels = None
depends_on = None


def upgrade():
    existing_tables = set(sa.inspect(op.get_bind()).get_table_names())

    if "exercises" not in existing_tables:
        op.create_table(
            "exercises",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False),
            sa.Column("category", sa.String(length=50), nullable=False),
            sa.Column("equipment_needed", sa.Boolean(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name", name="unique_exercise_name"),
        )

    if "workouts" not in existing_tables:
        op.create_table(
            "workouts",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("date", sa.Date(), nullable=False),
            sa.Column("duration_minutes", sa.Integer(), nullable=False),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.CheckConstraint(
                "duration_minutes > 0",
                name="check_workout_duration_positive",
            ),
            sa.PrimaryKeyConstraint("id"),
        )

    if "workout_exercises" not in existing_tables:
        op.create_table(
            "workout_exercises",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("workout_id", sa.Integer(), nullable=False),
            sa.Column("exercise_id", sa.Integer(), nullable=False),
            sa.Column("reps", sa.Integer(), nullable=True),
            sa.Column("sets", sa.Integer(), nullable=True),
            sa.Column("duration_seconds", sa.Integer(), nullable=True),
            sa.CheckConstraint(
                "duration_seconds IS NULL OR duration_seconds > 0",
                name="check_exercise_duration_positive",
            ),
            sa.CheckConstraint(
                "reps IS NULL OR reps > 0",
                name="check_reps_positive",
            ),
            sa.CheckConstraint(
                "sets IS NULL OR sets > 0",
                name="check_sets_positive",
            ),
            sa.ForeignKeyConstraint(["exercise_id"], ["exercises.id"]),
            sa.ForeignKeyConstraint(["workout_id"], ["workouts.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "workout_id",
                "exercise_id",
                name="unique_workout_exercise",
            ),
        )


def downgrade():
    # Keep the baseline schema intact when reverting this repair revision.
    pass
