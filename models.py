"""
Core data models for the Timetable Generator System.
"""

class TimeSlot:
    """Represents a time slot in the timetable."""
    
    def __init__(self, day, period, start_time, end_time):
        self.day = day
        self.period = period
        self.start_time = start_time
        self.end_time = end_time
    
    def __str__(self):
        return f"{self.day} Period {self.period} ({self.start_time}-{self.end_time})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return (self.day == other.day and 
                self.period == other.period)
    
    def __hash__(self):
        return hash((self.day, self.period))


class Room:
    """Represents a classroom or lab."""
    
    def __init__(self, room_id, name, capacity, room_type="classroom"):
        self.room_id = room_id
        self.name = name
        self.capacity = capacity
        self.room_type = room_type
    
    def __str__(self):
        return f"{self.name} (Cap: {self.capacity})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.room_id == other.room_id
    
    def __hash__(self):
        return hash(self.room_id)


class Teacher:
    """Represents a teaching faculty member."""
    
    def __init__(self, teacher_id, name, department, specializations=None):
        self.teacher_id = teacher_id
        self.name = name
        self.department = department
        self.specializations = specializations or []
        self.unavailable_slots = set()
    
    def add_unavailable_slot(self, time_slot):
        """Mark a time slot as unavailable for this teacher."""
        self.unavailable_slots.add(time_slot)
    
    def is_available(self, time_slot):
        """Check if teacher is available at given time slot."""
        return time_slot not in self.unavailable_slots
    
    def __str__(self):
        return f"{self.name} ({self.department})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.teacher_id == other.teacher_id
    
    def __hash__(self):
        return hash(self.teacher_id)


class Course:
    """Represents a course/subject."""
    
    def __init__(self, course_id, name, department, hours_per_week, course_type="theory"):
        self.course_id = course_id
        self.name = name
        self.department = department
        self.hours_per_week = hours_per_week
        self.course_type = course_type
    
    def __str__(self):
        return f"{self.name} ({self.course_id})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.course_id == other.course_id
    
    def __hash__(self):
        return hash(self.course_id)


class Section:
    """Represents a student section/group."""
    
    def __init__(self, section_id, name, department, semester, student_count):
        self.section_id = section_id
        self.name = name
        self.department = department
        self.semester = semester
        self.student_count = student_count
    
    def __str__(self):
        return f"{self.name} (Sem {self.semester})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.section_id == other.section_id
    
    def __hash__(self):
        return hash(self.section_id)


class ClassAssignment:
    """Represents a scheduled class in the timetable."""
    
    def __init__(self, course, section, teacher, room, time_slot):
        self.course = course
        self.section = section
        self.teacher = teacher
        self.room = room
        self.time_slot = time_slot
    
    def __str__(self):
        return (f"{self.course.name} | {self.section.name} | "
                f"{self.teacher.name} | {self.room.name} | {self.time_slot}")
    
    def __repr__(self):
        return self.__str__()
