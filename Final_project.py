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


