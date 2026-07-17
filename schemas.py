from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError

from models import Workout, Exercise, WorkoutExercise


class WorkoutExerciseSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True

    exercise = fields.Nested(
        "ExerciseSchema",
        only=("id", "name", "category", "equipment_needed")
    )


class WorkoutSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Workout
        load_instance = True

    workout_exercises = fields.Nested(
        "WorkoutExerciseSchema",
        many=True
    )

    @validates("duration_minutes")
    def validate_duration(self, value):

        if value <= 0:
            raise ValidationError(
                "Duration must be greater than 0 minutes."
            )


class ExerciseSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Exercise
        load_instance = True

    workout_exercises = fields.Nested(
        "WorkoutExerciseSchema",
        many=True,
        exclude=("exercise",)
    )

    @validates("name")
    def validate_name(self, value):

        if len(value.strip()) < 2:
            raise ValidationError(
                "Exercise name must contain at least 2 characters."
            )



workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)