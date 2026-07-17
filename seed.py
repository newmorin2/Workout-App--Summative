#!/usr/bin/env python3

from datetime import date
from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():

	# reset data and add new example data, committing to db

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    push_up = Exercise(
        name="Push Up",
        category="Chest",
        equipment_needed=False
    )

    squat = Exercise(
        name="Squat",
        category="Legs",
        equipment_needed=False
    )

    plank = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False
    )

    bench_press = Exercise(
        name="Bench Press",
        category="Chest",
        equipment_needed=True
    )

    db.session.add_all([push_up, squat, plank, bench_press])
    db.session.commit()

    workout1 = Workout(
        date=date(2026, 7, 17),
        duration_minutes=60,
        notes="Upper body workout"
    )

    workout2 = Workout(
        date=date(2026, 7, 18),
        duration_minutes=45,
        notes="Leg day"
    )

    db.session.add_all([workout1, workout2])
    db.session.commit()

    we1 = WorkoutExercise(
        workout=workout1,
        exercise=push_up,
        sets=3,
        reps=15,
        duration_seconds=None
    )

    we2 = WorkoutExercise(
        workout=workout1,
        exercise=bench_press,
        sets=4,
        reps=10,
        duration_seconds=None
    )

    we3 = WorkoutExercise(
        workout=workout2,
        exercise=squat,
        sets=4,
        reps=12,
        duration_seconds=None
    )

    we4 = WorkoutExercise(
        workout=workout2,
        exercise=plank,
        sets=None,
        reps=None,
        duration_seconds=60
    )

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print("Database seeded successfully!")