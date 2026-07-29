from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    print('Clearing old data...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print('Creating exercises...')
    push_up = Exercise(name='Push Up', category='Strength', equipment_needed=False)
    squat = Exercise(name='Squat', category='Strength', equipment_needed=False)
    plank = Exercise(name='Plank', category='Core', equipment_needed=False)
    bench_press = Exercise(name='Bench Press', category='Strength', equipment_needed=True)
    running = Exercise(name='Running', category='Cardio', equipment_needed=False)

    db.session.add_all([push_up, squat, plank, bench_press, running])
    db.session.commit()

    print('Creating workouts...')
    workout_1 = Workout(date='2026-07-01', duration_minutes=45, notes='Morning strength session')
    workout_2 = Workout(date='2026-07-03', duration_minutes=30, notes='Core and cardio')
    workout_3 = Workout(date='2026-07-05', duration_minutes=60, notes='Full body workout')

    db.session.add_all([workout_1, workout_2, workout_3])
    db.session.commit()

    print('Creating workout_exercises...')
    workout_exercises = [
        WorkoutExercise(workout_id=workout_1.id, exercise_id=push_up.id, reps=15, sets=3),
        WorkoutExercise(workout_id=workout_1.id, exercise_id=squat.id, reps=12, sets=3),
        WorkoutExercise(workout_id=workout_2.id, exercise_id=plank.id, sets=3, duration_seconds=60),
        WorkoutExercise(workout_id=workout_2.id, exercise_id=running.id, sets=1, duration_seconds=1200),
        WorkoutExercise(workout_id=workout_3.id, exercise_id=bench_press.id, reps=10, sets=4),
        WorkoutExercise(workout_id=workout_3.id, exercise_id=push_up.id, reps=20, sets=2),
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print('Seeding complete!')
