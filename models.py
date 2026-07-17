from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here
class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    @validates("sets", "reps", "duration_seconds")
    def validate_numbers(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f"{key} must be greater than 0.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "workout_id": self.workout_id,
            "exercise_id": self.exercise_id,
            "sets": self.sets,
            "reps": self.reps,
            "duration_seconds": self.duration_seconds
        }


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be greater than 0.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "duration_minutes": self.duration_minutes,
            "notes": self.notes
        }


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Exercise name cannot be empty.")
        return value

    @validates("category")
    def validate_category(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Category cannot be empty.")
        return value

    @validates("equipment_needed")
    def validate_equipment(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("equipment_needed must be True or False.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "equipment_needed": self.equipment_needed
        }