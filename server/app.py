import os

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema, ExerciseDetailSchema,
    WorkoutSchema, WorkoutDetailSchema,
    WorkoutExerciseSchema,
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

workout_exercise_schema = WorkoutExerciseSchema()


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Workout Tracker API'})


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify(workout_detail_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    try:
        validated = workout_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    try:
        workout = Workout(
            date=validated['date'],
            duration_minutes=validated['duration_minutes'],
            notes=validated.get('notes'),
        )
        db.session.add(workout)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 400

    return jsonify(workout_schema.dump(workout)), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404

    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout deleted'}), 200


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify(exercise_detail_schema.dump(exercise)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()

    try:
        validated = exercise_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    try:
        exercise = Exercise(
            name=validated['name'],
            category=validated.get('category'),
            equipment_needed=validated.get('equipment_needed', False),
        )
        db.session.add(exercise)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 400

    return jsonify(exercise_schema.dump(exercise)), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted'}), 200


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def create_workout_exercise(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    data = request.get_json() or {}

    try:
        validated = workout_exercise_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=validated.get('reps'),
            sets=validated.get('sets'),
            duration_seconds=validated.get('duration_seconds'),
        )
        db.session.add(workout_exercise)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 400

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad request'}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)
