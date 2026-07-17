from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from datetime import datetime
from models import db, Workout, Exercise, WorkoutExercise

from schemas import (
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)

    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = request.get_json()
        workout = workout_schema.load(data)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 400


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()

    return jsonify({
        "message": "Workout deleted successfully"
    }), 200



@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):

    exercise = Exercise.query.get_or_404(id)

    return exercise_schema.jsonify(exercise), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = request.get_json()
        exercise = exercise_schema.load(data)
        db.session.add(exercise)
        db.session.commit()

        return exercise_schema.jsonify(exercise), 201


    except Exception as e:
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 400


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise deleted successfully"
    }), 200



@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        workout = Workout.query.get_or_404(workout_id)
        exercise = Exercise.query.get_or_404(exercise_id)
        data = request.get_json()

        workout_exercise = workout_exercise_schema.load(data)
        workout_exercise.workout = workout
        workout_exercise.exercise = exercise
        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201

    except Exception as e:

        db.session.rollback()
        return jsonify({
            "error": str(e)
        }), 400



if __name__ == '__main__':
    app.run(port=5555, debug=True)