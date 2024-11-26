# Class representing the user
class User:
    def __init__(self, name,calories):
        self.name = name
        self.workouts = []
        self.calories = 0
    def add_workout(self, workout):
        self.workouts.append(workout)
        self.calories += workout.calories_burned
# Class representing a log of a workout
class Workout:
    def __init__(self):
        self.exercises = []
        self.calories_burned = 0
    def add_exercise(self, exercise):
        self.exercises.append(exercise)
        self.calories_burned += exercise.calculate_calories_burned()
# Class representing a single exercise
class Exercise:
    def __init__(self, name, muscle_group, duration, calories_burned_per_minute):
        self.name = name
        self.muscle_group = muscle_group
        self.duration = duration
        self.calories_burned_per_minute = calories_burned_per_minute
    def calculate_calories_burned(self):
        return self.duration * self.calories_burned_per_minute
# Main function that starts the program up with user input to figure out what the user wants to do
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
# Function that suggests workouts based on the muscle group entered by the user
# Function that suggests workouts based on the muscle group entered by the user
def workout_suggester(muscle_group):
  pass
  #Need to write code that prints out exercise suggestions based off a database that we create of potential workouts and muscle groups that they target.
# Function that logs a workout for a specific user
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
  #Need to write code that collects data from the user and logs it into a database. We want to collect their name, exercise, duration, etc.
#Planned Unit Test:
#Test that the workout suggester function works as intended
#Test that the log workout function works as intended
#Test that the main function works as intended
  #Specifically I will test that the main function starts the program up and that the user can choose to log a workout or get workout suggestions
#Test that the User class works as intended
  #Specifically I will test that the User class has the correct attributes and methods and properly tracks a user progress
#Test that the Workout class works as intended
  #Specifically I will test that the Workout class to make sure workouts are correctly recorded
#Test that the Exercise class works as intended
  #Specifically I will test that the Exercise class by inputting the correct attributes from a database of exercises that we will create later on.
#We have to either scrape a list of exercises online or create our own list of exercises that we can use to test and create the program