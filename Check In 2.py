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

