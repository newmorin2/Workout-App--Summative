# Project title
Workout App

# Project description
The Workout Tracking API is a backend application built with Flask and SQLAlchemy that allows personal trainers to manage workouts and exercises.

The API will be responsible for tracking workouts and their associated exercises. Each workout can include multiple exercises, with sets, reps, or duration attached to each. Exercises need to be reusable so a trainer can add the same exercise to various workouts.

The application uses:
- Flask for the API framework
- SQLAlchemy for database management
- Flask-Migrate for database migrations
- Marshmallow for serialization, deserialization, and validation
- SQLite as the database

# Installation Instructions

## 1. Clone the repository

```bash
git clone https://github.com/newmorin2/Workout-App--Summative

cd Workout-App--Summative
```

## 2. Install dependencies
Install packages:

-pip install requirements.txt

Create the virtual environment:

-python3 -m venv venv

Activate the virtual environment:

-source venv/bin/activate

## 3. Seed the database
python3 seed.py

## 4. Run the server
- python3 app.py

# API Endpoints

## Workouts

GET /workouts
- Returns a list of all workouts.

GET /workouts/<id>
- Returns a single workout with its associated exercises

POST /workouts
- Creates a new workout

DELETE /workouts/<id>
- Deletes a workout

## Exercises
GET /exercises
- Returns all exercises.

GET /exercises/<id>
- Returns a single exercise and associated workout information

POST /exercises
- Creates a new exercise

DELETE /exercises/<id>
- Deletes an exercise.

## Workout Exercise
POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises

Adds an exercise to a workout.
This endpoint creates the relationship between a workout and an exercise while storing workout-specific information.