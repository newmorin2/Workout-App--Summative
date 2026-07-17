from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import validates, ValidationError

from models import Workout, Exercise, WorkoutExercise


class WorkoutSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Workout
        load_instance = True

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

    @validates("name")
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise ValidationError(
                "Exercise name must contain at least 2 characters."
            )


class WorkoutExerciseSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = WorkoutExercise
        load_instance = True


# Schema instances
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)