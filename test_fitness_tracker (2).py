
import unittest
import datetime
import json
from fitness_tracker import Exercise, Workout, User, workout_suggester



class TestExercise(unittest.TestCase):
    def setUp(self):
        self.exercise = Exercise(
            name="Push-ups",
            muscle_group="Upper Body",
            duration=10,
            calories_burned_per_minute=5.0,
            intensity="medium",
            equipment_needed=["mat"]
        )

    def test_exercise_initialization(self):
        self.assertEqual(self.exercise.name, "Push-ups")
        self.assertEqual(self.exercise.muscle_group, "Upper Body")
        self.assertEqual(self.exercise.duration, 10)
        self.assertEqual(self.exercise.calories_burned_per_minute, 5.0)
        self.assertEqual(self.exercise.intensity, "medium")
        self.assertEqual(self.exercise.equipment_needed, ["mat"])

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            Exercise("Push-ups", "Upper Body", -1, 5.0)

    def test_invalid_calories(self):
        with self.assertRaises(ValueError):
            Exercise("Push-ups", "Upper Body", 10, -5.0)

    def test_invalid_intensity(self):
        with self.assertRaises(ValueError):
            Exercise("Push-ups", "Upper Body", 10, 5.0, intensity="invalid")

    def test_calculate_calories_burned(self):
        # Test with just weight
        calories = self.exercise.calculate_calories_burned(70)
        self.assertEqual(calories, 50.0)  # 10 min * 5.0 cal/min * (70/70)

        # Test with weight and heart rate
        calories = self.exercise.calculate_calories_burned(70, heart_rate=150)
        self.assertEqual(calories, 60.0)  # 50.0 * 1.2 (heart rate factor)

class TestWorkout(unittest.TestCase):
    def setUp(self):
        self.workout = Workout()
        self.exercise = Exercise(
            "Push-ups",
            "Upper Body",
            10,
            5.0,
            "medium",
            ["mat"]
        )

    def test_workout_initialization(self):
        self.assertEqual(len(self.workout.exercises), 0)
        self.assertEqual(self.workout._total_duration, 0)
        self.assertEqual(self.workout._total_calories_burned, 0)
        self.assertEqual(len(self.workout.heart_rate_log), 0)

    def test_add_exercise(self):
        self.workout.add_exercise(self.exercise, 70, heart_rate=150)
        
        self.assertEqual(len(self.workout.exercises), 1)
        self.assertEqual(self.workout._total_duration, 10)
        self.assertEqual(self.workout._total_calories_burned, 60.0)
        self.assertEqual(self.workout.heart_rate_log, [150])

    def test_get_workout_summary(self):
        self.workout.add_exercise(self.exercise, 70, heart_rate=150)
        summary = self.workout.get_workout_summary()
        
        self.assertEqual(summary["exercise_count"], 1)
        self.assertEqual(summary["total_duration"], 10)
        self.assertEqual(summary["total_calories"], 60.0)
        self.assertEqual(summary["muscle_groups"], ["Upper Body"])
        self.assertEqual(summary["equipment_used"], ["mat"])
        self.assertEqual(summary["average_heart_rate"], 150)

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(
            name="John",
            weight=70,
            height=175,
            age=30,
            fitness_level="intermediate"
        )
        self.workout = Workout()
        self.exercise = Exercise(
            "Push-ups",
            "Upper Body",
            10,
            5.0,
            "medium",
            ["mat"]
        )

    def test_user_initialization(self):
        self.assertEqual(self.user.name, "John")
        self.assertEqual(self.user.weight, 70)
        self.assertEqual(self.user.height, 175)
        self.assertEqual(self.user.age, 30)
        self.assertEqual(self.user.fitness_level, "intermediate")
        self.assertEqual(len(self.user.workouts), 0)
        self.assertEqual(len(self.user.goals), 0)
        self.assertEqual(len(self.user.progress_history), 0)

    def test_add_workout(self):
        self.workout.add_exercise(self.exercise, self.user.weight)
        self.user.add_workout(self.workout)
        
        self.assertEqual(len(self.user.workouts), 1)
        self.assertEqual(len(self.user.progress_history), 1)
        
        progress = self.user.progress_history[0]
        self.assertEqual(progress["calories"], 50.0)
        self.assertEqual(progress["duration"], 10)

    def test_set_goal(self):
        deadline = datetime.date.today() + datetime.timedelta(days=30)
        self.user.set_goal("calories", 1000, deadline)
        
        self.assertIn("calories", self.user.goals)
        self.assertEqual(self.user.goals["calories"]["target"], 1000)
        self.assertEqual(self.user.goals["calories"]["deadline"], deadline)

class TestWorkoutSuggester(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            "Upper Body": [
                {
                    "name": "Push-ups",
                    "duration": 10,
                    "calories_burned_per_minute": 5.0,
                    "intensity": "medium",
                    "equipment_needed": ["mat"]
                }
            ]
        }
        # Create a temporary exercise database file for testing
        with open('test_exercise_database.json', 'w') as f:
            json.dump(self.test_data, f)

    def test_workout_suggester(self):
        suggestions = workout_suggester(
            muscle_group="Upper Body",
            user_weight=70,
            fitness_level="intermediate",
            available_equipment=["mat"]
        )
        
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0]["name"], "Push-ups")
        self.assertEqual(suggestions[0]["duration"], 10)
        self.assertEqual(suggestions[0]["calories_per_minute"], 5.0)

    def test_workout_suggester_no_equipment(self):
        suggestions = workout_suggester(
            muscle_group="Upper Body",
            user_weight=70,
            fitness_level="intermediate",
            available_equipment=["dumbbell"]  # Equipment not matching test data
        )
        
        self.assertEqual(len(suggestions), 0)

    def tearDown(self):
        import os
        # Clean up the temporary test file
        try:
            os.remove('test_exercise_database.json')
        except:
            pass

if __name__ == '__main__':
    unittest.main()
