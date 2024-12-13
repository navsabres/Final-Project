import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import time

#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='fitness_tracker.log'
)

class Exercise:
    """
    Represents a single exercise with its properties and methods.
    """
    def __init__(self, name: str, muscle_group: str, duration: int, 
                 calories_burned_per_minute: float, intensity: str = "medium",
                 equipment_needed: List[str] = None):
        self.name = name
        self.muscle_group = muscle_group
        self.duration = duration
        self.calories_burned_per_minute = calories_burned_per_minute
        self.intensity = intensity
        self.equipment_needed = equipment_needed or []
        self.validate()

    def validate(self):
        """Validates exercise attributes."""
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if self.calories_burned_per_minute <= 0:
            raise ValueError("Calories burned must be positive")
        if self.intensity not in ["low", "medium", "high"]:
            raise ValueError("Invalid intensity level")

    def calculate_calories_burned(self, weight: float, heart_rate: Optional[int] = None) -> float:
        """Calculate calories burned considering weight and optional heart rate."""
        weight_factor = weight / 70
        base_calories = self.duration * self.calories_burned_per_minute * weight_factor

        intensity_multipliers = {"low": 0.8, "medium": 1.0, "high": 1.2}
        intensity_factor = intensity_multipliers[self.intensity]

        heart_rate_factor = 1.0
        if heart_rate:
            if heart_rate > 160:
                heart_rate_factor = 1.3
            elif heart_rate > 140:
                heart_rate_factor = 1.2
            elif heart_rate > 120:
                heart_rate_factor = 1.1

        return base_calories * intensity_factor * heart_rate_factor

class Workout:
    """
    Represents a complete workout session with multiple exercises.
    """
    def __init__(self):
        self.exercises = []
        self.date = datetime.now()
        self.notes = ""
        self._total_duration = 0
        self._total_calories_burned = 0
        self.heart_rate_log = []

    def add_exercise(self, exercise: Exercise, user_weight: float, heart_rate: Optional[int] = None):
        """Adding an exercise to the workout with heart rate tracking."""
        self.exercises.append(exercise)
        self._total_duration += exercise.duration
        calories = exercise.calculate_calories_burned(user_weight, heart_rate)
        self._total_calories_burned += calories
        
        if heart_rate:
            self.heart_rate_log.append(heart_rate)
            logging.info(f"Exercise added: {exercise.name} - Heart rate: {heart_rate}")

    def get_workout_summary(self) -> Dict:
        """Generating a detailed summary of the workout."""
        muscle_groups_worked = set(e.muscle_group for e in self.exercises)
        equipment_used = set(item for e in self.exercises 
                           for item in (e.equipment_needed or []))
        
        avg_heart_rate = None
        if self.heart_rate_log:
            avg_heart_rate = sum(self.heart_rate_log) / len(self.heart_rate_log)
        
        return {
            "date": self.date.strftime("%Y-%m-%d %H:%M"),
            "total_duration": self._total_duration,
            "total_calories": self._total_calories_burned,
            "exercise_count": len(self.exercises),
            "muscle_groups": list(muscle_groups_worked),
            "equipment_used": list(equipment_used),
            "average_heart_rate": avg_heart_rate,
            "notes": self.notes
        }

class User:
    """
    Represents a user of the fitness tracking system.
    """
    def __init__(self, name: str, weight: float, height: float = None, 
                 age: int = None, fitness_level: str = "intermediate"):
        self.name = name
        self.weight = weight
        self.height = height
        self.age = age
        self.fitness_level = fitness_level
        self.workouts = []
        self.goals = {}
        self.progress_history = []
        
        logging.info(f"New user created: {name}")

    def add_workout(self, workout: Workout):
        """Add a completed workout to user's history."""
        self.workouts.append(workout)
        self._update_progress_history(workout)
        self._check_goals(workout)
        
        logging.info(f"Workout added for {self.name}")

    def _update_progress_history(self, workout: Workout):
        """Track user's progress over time."""
        progress = {
            "date": workout.date,
            "calories": workout.get_workout_summary()["total_calories"],
            "duration": workout.get_workout_summary()["total_duration"]
        }
        self.progress_history.append(progress)

    def set_goal(self, goal_type: str, target: float, deadline: datetime.now().date()):
        """Set a fitness goal for the user."""
        self.goals[goal_type] = {
            "target": target,
            "deadline": deadline,
            "start_date": datetime.now().date(),
            "start_value": self._get_current_value(goal_type)
        }
        logging.info(f"New goal set for {self.name}: {goal_type} - {target}")

    def _get_current_value(self, goal_type: str) -> float:
        """Calculate current value for a given goal type."""
        if goal_type == "calories":
            return sum(w.get_workout_summary()["total_calories"] for w in self.workouts)
        elif goal_type == "workouts":
            return len(self.workouts)
        return 0

    def _check_goals(self, workout: Workout):
        """Check progress towards goals after each workout."""
        for goal_type, goal in self.goals.items():
            current = self._get_current_value(goal_type)
            progress = (current - goal["start_value"]) / (goal["target"] - goal["start_value"])
            if progress >= 1:
                logging.info(f"Goal achieved for {self.name}: {goal_type}")

    def view_workouts(self, detailed: bool = False):
        """View workout history with optional detailed analysis."""
        if not self.workouts:
            print(f"No workouts logged for {self.name}")
            return

        print(f"\nWorkout History for {self.name}")
        print(f"Weight: {self.weight} kg | Fitness Level: {self.fitness_level}")
        
        total_calories = sum(w.get_workout_summary()["total_calories"] for w in self.workouts)
        total_duration = sum(w.get_workout_summary()["total_duration"] for w in self.workouts)
        
        for i, workout in enumerate(self.workouts, 1):
            summary = workout.get_workout_summary()
            print(f"\nWorkout #{i} - {summary['date']}")
            print(f"Duration: {summary['total_duration']} minutes")
            print(f"Calories: {summary['total_calories']:.2f}")
            
            if detailed:
                print("Exercises:")
                for exercise in workout.exercises:
                    print(f"- {exercise.name} ({exercise.muscle_group})")
                    print(f"  Duration: {exercise.duration} min")
                    print(f"  Intensity: {exercise.intensity}")
                    if exercise.equipment_needed:
                        print(f"  Equipment: {', '.join(exercise.equipment_needed)}")

        print(f"\nTotal Statistics:")
        print(f"Total Workouts: {len(self.workouts)}")
        print(f"Total Duration: {total_duration} minutes")
        print(f"Total Calories: {total_calories:.2f}")

    def view_progress(self):
        """Display user's progress in a text-based format."""
        if not self.progress_history:
            print("Not enough data for progress report")
            return

        print(f"\nProgress Report for {self.name}")
        print("-" * 40)
        
        # Calculate trends
        calories_trend = [p["calories"] for p in self.progress_history]
        duration_trend = [p["duration"] for p in self.progress_history]
        
        print("Calories Burned Trend:")
        for i, calories in enumerate(calories_trend):
            print(f"Workout {i+1}: {calories:.1f} calories")
        
        print("\nWorkout Duration Trend:")
        for i, duration in enumerate(duration_trend):
            print(f"Workout {i+1}: {duration} minutes")
        
        # Calculate averages
        avg_calories = sum(calories_trend) / len(calories_trend)
        avg_duration = sum(duration_trend) / len(duration_trend)
        
        print(f"\nAverage calories per workout: {avg_calories:.1f}")
        print(f"Average duration per workout: {avg_duration:.1f} minutes")

def clear_screen(pause: bool = False):
    """
    Clear the terminal screen.
    Optional: Pause before clearing.
    """
    if pause:
        input("\nPress Enter to continue..")
    os.system('cls' if os.name == 'nt' else 'clear')

def log_workout(workout, user, exercise_name, muscle_group, duration, intensity, calories_per_min, heart_rate):
    """
    Adds an exercise to the workout with validation
    """
    try:
        #Validate numeric inputs
        duration = int(duration)
        if duration <= 0:
            raise ValueError("Duration must be a positive number.")
        calories_per_min = float(calories_per_min)
        if calories_per_min <= 0:
            raise ValueError("Calories burned per minute must be positive.")
        if intensity not in ["low", "medium", "high"]:
            raise ValueError("Intensity must be low, medium, or high.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    #Load the exercise database
    try:
        with open('exercise_database.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load exercise database.")
        return

    #Match exercise
    found = False
    for group, exercises in data.items():
        for e in exercises:
            if e['name'].lower() == exercise_name.lower():  # Case-insensitive match
                exercise = Exercise(
                    name=e['name'],
                    muscle_group=group,
                    duration=duration,
                    calories_burned_per_minute=calories_per_min,
                    intensity=intensity,
                    equipment_needed=e.get('equipment_needed', [])
                )
                workout.add_exercise(exercise, user.weight, int(heart_rate) if heart_rate else None)
                print(f"=== Added {e['name']} ({duration} min) to the workout ===")
                found = True
                break
        if found:
            break

    #In case an exercise isn't in file, and user still wants to log
    if not found:
        print(f"\nExercise '{exercise_name}' not found.")
        #Prompt
        add_custom = input("\nWould you like to log this as a custom exercise? (yes/no): ").strip().lower()
        if add_custom == 'yes':
            print("\n=== Logging custom exercise ===")
            try:
                muscle_group = input("Enter muscle group: ").strip()
                duration = int(input("Enter duration (minutes): ").strip())
                calories_per_min = float(input("Enter calories burned per minute: ").strip())
                intensity = input("Enter intensity (low/medium/high): ").strip()
                custom_exercise = Exercise(
                    name=exercise_name,
                    muscle_group=muscle_group,
                    duration=duration,
                    calories_burned_per_minute=calories_per_min,
                    intensity=intensity
                )
                workout.add_exercise(custom_exercise, user.weight, int(heart_rate) if heart_rate else None)
                print(f"Custom exercise '{exercise_name}' added to the workout.")
            except ValueError as e:
                print(f"Invalid input: {e}. Custom exercise not added.")

def workout_suggester(muscle_group: str, user_weight: float, fitness_level: str = "intermediate",
                     available_equipment: List[str] = None) -> List[Dict]:
    """Suggest personalized exercises based on user's characteristics and equipment."""
    try:
        with open('exercise_database.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading exercise database: {e}")
        return []

    exercises = data.get(muscle_group, [])
    if not exercises:
        logging.warning(f"No exercises found for muscle group: {muscle_group}")
        return []

    if available_equipment:
        exercises = [e for e in exercises if not e.get('equipment_needed') or 
                    all(eq in available_equipment for eq in e['equipment_needed'])]

    difficulty_multipliers = {
        "beginner": 0.8,
        "intermediate": 1.0,
        "advanced": 1.2
    }
    multiplier = difficulty_multipliers.get(fitness_level, 1.0)

    suggestions = []
    for e in exercises:
        cal_adjusted = e['calories_burned_per_minute'] * (user_weight / 70) * multiplier
        suggestion = {
            'name': e['name'],
            'duration': e['duration'],
            'calories_per_minute': round(cal_adjusted, 2),
            'intensity': e.get('intensity', 'medium'),
            'equipment': e.get('equipment_needed', [])
        }
        suggestions.append(suggestion)

    return sorted(suggestions, key=lambda x: x['calories_per_minute'], reverse=True)

def main():
    
    users = {}


    #WELCOME SCREEN
    print("==============================================")
    print("\t   Welcome to Fitness Tracker Pro!")
    print("==============================================\n")
    print("Features:")
    print("\t- Log workouts")
    print("\t- Track progress")
    print("\t- Obtain personalized exercise suggestions\n")
    print("\033[1;31mNew Users: Start by logging a workout (Option 2) to create your profile.\033[0m")
    print("------------------------------------------------")

    #Pause before clearing
    input("Press Enter to continue...")

    while True:
        try:
            clear_screen()
            #MENU
            print("\n=== Fitness Tracker Menu ===")
            print("1: Get personalized workout suggestions")
            print("2: Log a workout")
            print("3: View workout history")
            print("4: Set fitness goals")
            print("5: View progress")
            print("q: Quit")
            
            choice = input("\033[1;34mChoose an option (1-5, q to quit): \033[0m").strip().lower()

            if choice == '1':  #WORKOUT SUGGESTIONS
                clear_screen()
                print("== Personalized Workout Suggestions ==")
                user_name = input("Enter your name (or type 'back' to return): ").strip()
                if not user_name or user_name not in users:
                    print("\033[1;31mUser not found. Please create a profile first.\033[0m")
                    input("\nPress Enter to return to the main menu.")
                    continue
                    
                user = users[user_name]
                muscle_group = input("Enter muscle group (Legs/Upper Body/Core, or type 'back' to return): ").strip()
                if muscle_group.lower() == 'back':
                    continue
                
                equipment = input("Available equipment (comma-separated, or press enter for none): ").strip()
                available_equipment = [e.strip() for e in equipment.split(',')] if equipment else None

                #UI Upgrade: Animation
                print("Fetching workout suggestions", end="", flush=True)
                for _ in range(3):
                    time.sleep(0.5)
                    print(".", end="", flush=True)
                print("\n")

                suggestions = workout_suggester(muscle_group, user.weight, user.fitness_level, available_equipment)
                clear_screen()

                if suggestions:
                    for s in suggestions:
                        print(f"\n{s['name']}:")
                        print(f"Duration: {s['duration']} min")
                        print(f"Calories/min: {s['calories_per_minute']}")
                        print(f"Intensity: {s['intensity']}")
                        if s['equipment']:
                            print(f"Equipment: {', '.join(s['equipment'])}")
                else:
                    print("\033[1;31mNo suggestions available for the given criteria.\033[0m")

                input("\nPress Enter to return to the main menu.")

            elif choice == '2':  #LOGGING A WORKOUT
                clear_screen()
                print("== Log a Workout ==")
                user_name = input("Enter your name (or type 'back' to return): ").strip()
                if user_name.lower() == 'back':
                    continue
                
                if not user_name:
                    print("\033[1;31mName cannot be empty.\033[0m")
                    input("\nPress Enter to return to the main menu.")
                    continue

                if user_name not in users:
                    try:
                        weight = float(input("Enter weight (kg): ").strip())
                        height = float(input("Enter height (cm): ").strip())
                        age = int(input("Enter age: ").strip())
                        fitness_level = input("Enter fitness level (beginner/intermediate/advanced): ").strip()
                        users[user_name] = User(user_name, weight, height, age, fitness_level)
                    except ValueError as e:
                        print(f"\033[1;31mInvalid input: {e}\033[0m")
                        input("\nPress Enter to return to the main menu.")
                        continue

                user = users[user_name]
                workout = Workout()
                print("\n=== Logging workout (type 'done' when finished) ===")

                while True:
                    exercise_name = input("\nEnter exercise name (or 'done' to finish): ").strip()
                    if exercise_name.lower() == 'done':
                        break
                    if exercise_name.lower() == 'back':
                        continue

                    muscle_group = input("Enter muscle group (Legs/Upper Body/Core): ").strip()
                    duration = input("Enter duration (minutes): ").strip()
                    intensity = input("Enter intensity (low/medium/high): ").strip()
                    calories_per_min = input("Enter calories burned per minute: ").strip()
                    heart_rate = input("Heart rate (optional): ").strip()

                    #Pass inputs to log_workout
                    log_workout(workout, user, exercise_name, muscle_group, duration, intensity, calories_per_min, heart_rate)

                workout.notes = input("\nAny notes for this workout? ").strip()
                user.add_workout(workout)
                print("\033[1;32mWorkout logged successfully!\033[0m")
                input("\nPress Enter to return to the main menu.")


            elif choice == '3':  #VIEW WORKOUT HISTORY
                clear_screen()
                print("== View Workout History ==")
                user_name = input("Enter your name (or type 'back' to return): ").strip()
                if user_name.lower() == 'back':
                    continue
                if user_name in users:
                    detailed = input("Show detailed view? (y/n): ").strip().lower() == 'y'
                    users[user_name].view_workouts(detailed)
                else:
                    print("\033[1;31mUser not found.\033[0m")
                input("\nPress Enter to return to the main menu.")

            elif choice == '4':  #SET FITNESS GOALS
                clear_screen()
                print("== Set Fitness Goals ==")
                user_name = input("Enter your name (or type 'back' to return): ").strip()
                if user_name.lower() == 'back':
                    continue
                if user_name not in users:
                    print("\033[1;31mUser not found.\033[0m")
                    input("\nPress Enter to return to the main menu.")
                    continue

                goal_type = input("Goal type (calories/workouts): ").strip()
                target = float(input("Target value: ").strip())
                days = int(input("Days to achieve goal: ").strip())
                deadline = datetime.now().date() + timedelta(days=days)

                users[user_name].set_goal(goal_type, target, deadline)
                print("\033[1;32mGoal set successfully!\033[0m")
                input("\nPress Enter to return to the main menu.")

            elif choice == '5':  # VIEW PROGRESS
                clear_screen()
                print("== View Progress ==")
                user_name = input("Enter your name (or type 'back' to return): ").strip()
                if user_name.lower() == 'back':
                    continue
                if user_name in users:
                    users[user_name].view_progress()
                else:
                    print("\033[1;31mUser not found.\033[0m")
                input("\nPress Enter to return to the main menu.")

            elif choice == 'q':  #Quit the app
                confirm = input("Are you sure you want to quit? (y/n): ").strip().lower()
                if confirm == 'y':
                    clear_screen()
                    print("\033[1;32mThank you for using Fitness Tracker Pro!\033[0m")
                    break

            else:
                clear_screen()
                print("Returning to the main menu...")
                continue

        except Exception as e:
            print(f"\033[1;31mAn error occurred: {e}\033[0m")
            input("\nPress Enter to return to the main menu.")

if __name__ == "__main__":
    main()