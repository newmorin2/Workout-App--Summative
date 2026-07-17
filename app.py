from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Workout, Exercise, WorkoutExercise

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here
@app.route("/workouts", methods=["GET"])
def get_workouts():

    workouts = Workout.query.all()

    workout_list = []

    for workout in workouts:
        workout_list.append({
            "id": workout.id,
            "date": workout.date.isoformat(),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        })

    return jsonify(workout_list), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):

    workout = Workout.query.get_or_404(id)

    exercises = []

    for we in workout.workout_exercises:
        exercises.append({
            "id": we.exercise.id,
            "name": we.exercise.name,
            "category": we.exercise.category,
            "sets": we.sets,
            "reps": we.reps,
            "duration_seconds": we.duration_seconds
        })

    return jsonify({
        "id": workout.id,
        "date": workout.date.isoformat(),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "exercises": exercises
    }), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):

    workout = Workout.query.get_or_404(id)

    exercises = []

    for we in workout.workout_exercises:
        exercises.append({
            "id": we.exercise.id,
            "name": we.exercise.name,
            "category": we.exercise.category,
            "sets": we.sets,
            "reps": we.reps,
            "duration_seconds": we.duration_seconds
        })

    return jsonify({
        "id": workout.id,
        "date": workout.date.isoformat(),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "exercises": exercises
    }), 200


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

    exercise_list = []

    for exercise in exercises:

        exercise_list.append({
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        })

    return jsonify(exercise_list), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):

    exercise = Exercise.query.get_or_404(id)

    workouts = []

    for we in exercise.workout_exercises:
        workouts.append({
            "id": we.workout.id,
            "date": we.workout.date.isoformat(),
            "duration_minutes": we.workout.duration_minutes
        })

    return jsonify({
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed,
        "workouts": workouts
    }), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():

    data = request.get_json()

    exercise = Exercise(
        name=data["name"],
        category=data["category"],
        equipment_needed=data["equipment_needed"]
    )

    db.session.add(exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise created successfully",
        "id": exercise.id
    }), 201

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):

    exercise = Exercise.query.get_or_404(id)

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise deleted successfully"
    }), 200


@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise(workout_id, exercise_id):

    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)

    data = request.get_json()

    workout_exercise = WorkoutExercise(
        workout=workout,
        exercise=exercise,
        reps=data.get("reps"),
        sets=data.get("sets"),
        duration_seconds=data.get("duration_seconds")
    )

    db.session.add(workout_exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise added to workout successfully."
    }), 201



if __name__ == '__main__':
    app.run(port=5555, debug=True)