"""
Configuration system for institution-specific rules and settings.
"""

import json


class TimetableConfig:
    """Configuration for timetable generation with customizable rules."""
    
    def __init__(self):
        # Default time slots configuration
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.periods_per_day = 6
        self.period_duration = 60  # minutes
        
        # Time slot definitions
        self.time_slots = {
            1: ("09:00", "10:00"),
            2: ("10:00", "11:00"),
            3: ("11:00", "12:00"),
            4: ("12:00", "13:00"),
            5: ("14:00", "15:00"),
            6: ("15:00", "16:00")
        }
        
        # Scheduling rules
        self.max_classes_per_day = 6
        self.min_break_between_classes = 0  # periods
        self.max_consecutive_classes = 3
        
        # Course distribution rules
        self.prefer_morning_for_core = True
        self.avoid_single_class_days = True
        self.distribute_evenly = True
        
        # Room preferences
        self.prefer_department_rooms = True
        self.lab_courses_require_labs = True
        
        # Optimization weights
        self.weight_no_gaps = 0.3
        self.weight_teacher_preference = 0.2
        self.weight_compact_schedule = 0.3
        self.weight_room_distance = 0.2
    
    def load_from_file(self, filepath):
        """Load configuration from JSON file."""
        try:
            with open(filepath, 'r') as f:
                config_data = json.load(f)
                self._apply_config(config_data)
            return True
        except FileNotFoundError:
            print(f"Config file not found: {filepath}")
            return False
        except json.JSONDecodeError:
            print(f"Invalid JSON in config file: {filepath}")
            return False
    
    def save_to_file(self, filepath):
        """Save current configuration to JSON file."""
        config_data = {
            "days": self.days,
            "periods_per_day": self.periods_per_day,
            "period_duration": self.period_duration,
            "time_slots": {str(k): v for k, v in self.time_slots.items()},
            "max_classes_per_day": self.max_classes_per_day,
            "min_break_between_classes": self.min_break_between_classes,
            "max_consecutive_classes": self.max_consecutive_classes,
            "prefer_morning_for_core": self.prefer_morning_for_core,
            "avoid_single_class_days": self.avoid_single_class_days,
            "distribute_evenly": self.distribute_evenly,
            "prefer_department_rooms": self.prefer_department_rooms,
            "lab_courses_require_labs": self.lab_courses_require_labs,
            "optimization_weights": {
                "no_gaps": self.weight_no_gaps,
                "teacher_preference": self.weight_teacher_preference,
                "compact_schedule": self.weight_compact_schedule,
                "room_distance": self.weight_room_distance
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        return True
    
    def _apply_config(self, config_data):
        """Apply configuration data to current instance."""
        if "days" in config_data:
            self.days = config_data["days"]
        if "periods_per_day" in config_data:
            self.periods_per_day = config_data["periods_per_day"]
        if "period_duration" in config_data:
            self.period_duration = config_data["period_duration"]
        if "time_slots" in config_data:
            self.time_slots = {int(k): tuple(v) for k, v in config_data["time_slots"].items()}
        if "max_classes_per_day" in config_data:
            self.max_classes_per_day = config_data["max_classes_per_day"]
        if "min_break_between_classes" in config_data:
            self.min_break_between_classes = config_data["min_break_between_classes"]
        if "max_consecutive_classes" in config_data:
            self.max_consecutive_classes = config_data["max_consecutive_classes"]
        if "prefer_morning_for_core" in config_data:
            self.prefer_morning_for_core = config_data["prefer_morning_for_core"]
        if "avoid_single_class_days" in config_data:
            self.avoid_single_class_days = config_data["avoid_single_class_days"]
        if "distribute_evenly" in config_data:
            self.distribute_evenly = config_data["distribute_evenly"]
        if "prefer_department_rooms" in config_data:
            self.prefer_department_rooms = config_data["prefer_department_rooms"]
        if "lab_courses_require_labs" in config_data:
            self.lab_courses_require_labs = config_data["lab_courses_require_labs"]
        if "optimization_weights" in config_data:
            weights = config_data["optimization_weights"]
            self.weight_no_gaps = weights.get("no_gaps", self.weight_no_gaps)
            self.weight_teacher_preference = weights.get("teacher_preference", self.weight_teacher_preference)
            self.weight_compact_schedule = weights.get("compact_schedule", self.weight_compact_schedule)
            self.weight_room_distance = weights.get("room_distance", self.weight_room_distance)
    
    def get_all_time_slots(self):
        """Generate all possible time slots based on configuration."""
        from models import TimeSlot
        
        slots = []
        for day in self.days:
            for period in range(1, self.periods_per_day + 1):
                if period in self.time_slots:
                    start, end = self.time_slots[period]
                    slots.append(TimeSlot(day, period, start, end))
        return slots
    
    def __str__(self):
        return (f"TimetableConfig(days={len(self.days)}, "
                f"periods={self.periods_per_day}, "
                f"max_classes={self.max_classes_per_day})")
