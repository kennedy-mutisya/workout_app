from marshmallow import Schema, fields, validate, validates, ValidationError


class WorkoutBriefSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(dump_only=True)
    duration_minutes = fields.Integer(dump_only=True)
    notes = fields.String(dump_only=True, allow_none=True)


class ExerciseBriefSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    category = fields.String(dump_only=True)
    equipment_needed = fields.Boolean(dump_only=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)
    reps = fields.Integer(
        allow_none=True, validate=validate.Range(min=1), load_default=None
    )
    sets = fields.Integer(
        allow_none=True, validate=validate.Range(min=1), load_default=None
    )
    duration_seconds = fields.Integer(
        allow_none=True, validate=validate.Range(min=1), load_default=None
    )
    exercise = fields.Nested(ExerciseBriefSchema, dump_only=True)


class ExerciseWorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    reps = fields.Integer(allow_none=True, dump_only=True)
    sets = fields.Integer(allow_none=True, dump_only=True)
    duration_seconds = fields.Integer(allow_none=True, dump_only=True)
    workout = fields.Nested(WorkoutBriefSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1))

    notes = fields.String(allow_none=True, load_default=None)

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)

    name = fields.String(required=True, validate=validate.Length(min=1, max=100))

    category = fields.String(required=True, validate=validate.Length(min=1, max=50))

    equipment_needed = fields.Boolean(load_default=False)

    workout_exercises = fields.Nested(ExerciseWorkoutSchema, many=True, dump_only=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Exercise name cannot be blank.")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Exercise category cannot be blank.")
