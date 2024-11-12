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

    while True:
        print("Welcome to the Fitness App")
        choice = input("Enter (1) get workout suggestions or (2) log a workout? Enter 'q' to quit: ")

        if choice == '1':
            muscle_group = input("Enter the muscle group you want to workout (Legs, Upper Body, Core): ")
            workout_suggester(muscle_group)

        elif choice == '2':
            user = input("Enter your name: ")
            log_workout(user)

        elif choice.lower() == 'q':
            print("Exiting the fitness tracker.")
            break
        else:
            print("Invalid. Please enter 1, 2, or q.")

# Function that suggests workouts based on the muscle group entered by the user
def workout_suggester(muscle_group):
  pass
  #Need to write code that prints out exercise suggestions based off a database that we create of potential workouts and muscle groups that they target.

# Function that logs a workout for a specific user
def log_workout(user):
  pass
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

