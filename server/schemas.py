from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error='Name must not be blank.')
    )
    category = fields.Str(
        validate=validate.Length(min=1, error='Category must not be empty.')
    )
    equipment_needed = fields.Bool()


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Str(
        required=True,
        validate=validate.Length(min=1, error='Date must not be blank.')
    )
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error='Duration must be positive.')
    )
    notes = fields.Str()


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(
        validate=validate.Range(min=0, error='Reps cannot be negative.'),
        allow_none=True
    )
    sets = fields.Int(
        validate=validate.Range(min=0, error='Sets cannot be negative.'),
        allow_none=True
    )
    duration_seconds = fields.Int(
        validate=validate.Range(min=0, error='Duration seconds cannot be negative.'),
        allow_none=True
    )
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)


class ExerciseDetailSchema(ExerciseSchema):
    workouts = fields.List(fields.Nested(WorkoutSchema), dump_only=True)
