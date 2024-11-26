import json

class User:
    def __init__(self, name, weight, calories= 0): #initialize with 0 (optional parameter)
        self.name = name
        self.weight = weight 
        self.workouts = [] #Storing user workouts
        self.calories = 0 #TOTAL calories burned

    def add_workout(self, workout):
        """
        Adding a workout to the user's history
        """
        self.workouts.append(workout)
        self.calories += workout.calories_burned 

  #POTENTIAL ADD ON??: Method to view workouts
    def view_workouts(self):
        """
          For each workout, this method lists:
          - Workout number
          - Total calories burned in the workout
          - Details of each exercise in the workout
        """
        if not self.workouts:  #If no workouts have been logged yet
            print(f"No workouts have been logged for {self.name}")
            return  
    
        print(f"\nWorkouts for {self.name} (Weight: {self.weight} kg):")
        workout_number = 1  #Tracking the workout number

        for workout in self.workouts:
            print(f"{workout_number}. Calories Burned: {workout.calories_burned}")
            print("   Exercises:")
            for exercise in workout.exercises:
                print(f"      - {exercise.name} ({exercise.muscle_group}): {exercise.duration} min, {exercise.calories_burned_per_minute} cal/min")
            workout_number += 1  # Increment the workout number after printing each workout
        print(f"Total Calories Burned Across All Workouts: {self.calories}")

def log_workout(user):
    try:
        with open('exercise_database.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load exercise database.")
        return
  
    workout = Workout()
    print(f"\nLogging a workout for {user.name}. Type 'done' when you're finished entering your exercises.")

    #Option to show available exercises if user isn't friendly with the app
    show_exercises = input("Would you like to see the available exercises? (yes/no): ").strip().lower()
    if show_exercises == 'yes':
        print("\nAvailable Exercises:")
        for muscle_group, exercises in data.items():
            print(f"\n{muscle_group.capitalize()}:")
            for e in exercises:
                print(f"  - {e['name']} ({e['duration']} min, {e['calories_burned_per_minute']} cal/min)")
    
    while True:
        exercise_name = input("\nEnter the exercise name, or type 'done': ").strip()
        if exercise_name.lower() == 'done':
            break

        #Searching for the exercise in the JSON data
        found = False
        for muscle_group, exercises in data.items():
            for e in exercises:
                if e['name'].lower() == exercise_name.lower():
                    #Duration of exercise performed
                    try:
                        duration = int(input(f"Enter the duration you performed {e['name']} (in minutes): ").strip())
                    except ValueError:
                        print("Invalid duration. Please enter a number.")
                        break

                    calories_per_minute = e['calories_burned_per_minute']
                    exercise = Exercise(e['name'], muscle_group, duration, calories_per_minute)
                    workout.add_exercise(exercise, user.weight)
                    print(f"Added {e['name']} ({duration} min) to the workout.")
                    found = True
                    break
            if found:
                break
        
        if not found:
            print(f"Error: Exercise '{exercise_name}' not found. Please try again.")

def main():
    users = {}  #Storing User objects by name

    while True:
        print("\n--- Welcome to the Fitness App! ---")
        print("1: Get workout suggestions")
        print("2: Log a workout")
        print("3: View logged workouts")
        print("q: Quit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            user_name = input("Enter your name: ").strip()
            if user_name not in users:
                print(f"No user data found for '{user_name}'. Please log a workout first.")
                continue
            muscle_group = input("Enter the muscle group (Legs, Upper Body, Core): ").strip()
            workout_suggester(muscle_group, users[user_name].weight)

        elif choice == '2':
            user_name = input("Enter your name: ").strip()
            if user_name not in users:
                try:
                    weight = float(input(f"Enter your weight in kg, {user_name}: ").strip())
                except ValueError:
                    print("Invalid weight. Please enter a number.")
                    continue
                users[user_name] = User(user_name, weight)
            log_workout(users[user_name])

        elif choice == '3':
            user_name = input("Enter your name: ").strip()
            if user_name in users:
                users[user_name].view_workouts()
            else:
                print(f"No data found for user '{user_name}'. Please log a workout first.")

        elif choice.lower() == 'q':
            print("Exiting the fitness tracker.")
            break
        else:
            print("Invalid. Please enter 1, 2, 3, or q.")
