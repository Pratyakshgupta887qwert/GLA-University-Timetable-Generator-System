"""
Core timetable generation engine with constraint-based scheduling.
"""

import random
from models import ClassAssignment
from constraints import ConstraintValidator, ConflictDetector


class TimetableGenerator:
    """
    Generates optimized timetables using constraint satisfaction and 
    backtracking algorithms.
    """
    
    def __init__(self, config):
        self.config = config
        self.validator = ConstraintValidator()
        self.assignments = []
        self.generation_stats = {
            'attempts': 0,
            'backtracks': 0,
            'conflicts_resolved': 0
        }
    
    def generate(self, courses, sections, teachers, rooms, course_assignments):
        """
        Generate a complete timetable.
        
        Args:
            courses: List of Course objects
            sections: List of Section objects
            teachers: List of Teacher objects
            rooms: List of Room objects
            course_assignments: Dict mapping (course_id, section_id) to teacher_id
        
        Returns:
            List of ClassAssignment objects or None if generation fails
        """
        print("Starting timetable generation...")
        self.assignments = []
        self.generation_stats = {'attempts': 0, 'backtracks': 0, 'conflicts_resolved': 0}
        
        # Build scheduling requests
        requests = self._build_scheduling_requests(
            courses, sections, teachers, course_assignments
        )
        
        # Sort requests by priority (harder to schedule first)
        requests = self._prioritize_requests(requests)
        
        # Get all available time slots
        all_slots = self.config.get_all_time_slots()
        
        # Try to schedule all requests
        success = self._schedule_requests(requests, rooms, all_slots)
        
        if success:
            print(f"\n✓ Timetable generated successfully!")
            print(f"  Total assignments: {len(self.assignments)}")
            print(f"  Attempts: {self.generation_stats['attempts']}")
            print(f"  Backtracks: {self.generation_stats['backtracks']}")
            
            # Verify no conflicts
            conflicts = ConflictDetector.find_all_conflicts(self.assignments)
            conflict_count = ConflictDetector.count_conflicts(conflicts)
            if conflict_count == 0:
                print(f"  ✓ No conflicts detected")
            else:
                print(f"  ⚠ Warning: {conflict_count} conflicts detected")
            
            return self.assignments
        else:
            print(f"\n✗ Failed to generate conflict-free timetable")
            print(f"  Attempts: {self.generation_stats['attempts']}")
            print(f"  Partial assignments: {len(self.assignments)}")
            return None
    
    def _build_scheduling_requests(self, courses, sections, teachers, course_assignments):
        """Build list of scheduling requests from input data."""
        requests = []
        
        # Create lookup dictionaries
        course_dict = {c.course_id: c for c in courses}
        section_dict = {s.section_id: s for s in sections}
        teacher_dict = {t.teacher_id: t for t in teachers}
        
        # Build requests for each course-section pair
        for (course_id, section_id), teacher_id in course_assignments.items():
            if course_id not in course_dict:
                print(f"Warning: Course {course_id} not found")
                continue
            if section_id not in section_dict:
                print(f"Warning: Section {section_id} not found")
                continue
            if teacher_id not in teacher_dict:
                print(f"Warning: Teacher {teacher_id} not found")
                continue
            
            course = course_dict[course_id]
            section = section_dict[section_id]
            teacher = teacher_dict[teacher_id]
            
            # Create multiple requests based on hours per week
            for i in range(course.hours_per_week):
                requests.append({
                    'course': course,
                    'section': section,
                    'teacher': teacher,
                    'instance': i + 1
                })
        
        return requests
    
    def _prioritize_requests(self, requests):
        """
        Prioritize scheduling requests (most constrained first).
        This improves the chances of finding a valid solution.
        """
        # Sort by multiple criteria
        def priority_key(req):
            # Lab courses are harder to schedule (fewer suitable rooms)
            lab_priority = 0 if req['course'].course_type == 'lab' else 1
            
            # Courses with fewer hours are easier to fit
            hours_priority = req['course'].hours_per_week
            
            # Sort by department to group related courses
            dept_priority = req['section'].department
            
            return (lab_priority, -hours_priority, dept_priority)
        
        return sorted(requests, key=priority_key)
    
    def _schedule_requests(self, requests, rooms, all_slots, max_attempts=10000):
        """
        Schedule all requests using constraint satisfaction with backtracking.
        """
        return self._backtrack_schedule(requests, 0, rooms, all_slots, max_attempts)
    
    def _backtrack_schedule(self, requests, index, rooms, all_slots, max_attempts):
        """
        Recursive backtracking algorithm to find valid schedule.
        """
        # Base case: all requests scheduled
        if index >= len(requests):
            return True
        
        # Check attempt limit
        if self.generation_stats['attempts'] >= max_attempts:
            return False
        
        request = requests[index]
        self.generation_stats['attempts'] += 1
        
        # Try to find valid slot and room for this request
        possible_assignments = self._get_possible_assignments(
            request, rooms, all_slots
        )
        
        # Try each possible assignment
        for assignment in possible_assignments:
            # Validate assignment
            is_valid, conflicts = self.validator.validate_assignment(
                assignment, self.assignments
            )
            
            if is_valid:
                # Add assignment and continue
                self.assignments.append(assignment)
                
                # Recursively schedule remaining requests
                if self._backtrack_schedule(requests, index + 1, rooms, all_slots, max_attempts):
                    return True
                
                # Backtrack if recursive call failed
                self.assignments.pop()
                self.generation_stats['backtracks'] += 1
        
        # No valid assignment found
        return False
    
    def _get_possible_assignments(self, request, rooms, all_slots):
        """
        Generate possible assignments for a request, ordered by preference.
        """
        course = request['course']
        section = request['section']
        teacher = request['teacher']
        
        # Filter suitable rooms
        suitable_rooms = self._filter_suitable_rooms(course, section, rooms)
        
        # Filter available slots
        available_slots = self._filter_available_slots(teacher, all_slots)
        
        # Generate all combinations
        assignments = []
        for room in suitable_rooms:
            for slot in available_slots:
                assignments.append(ClassAssignment(course, section, teacher, room, slot))
        
        # Shuffle to avoid patterns that might cause systematic failures
        random.shuffle(assignments)
        
        return assignments
    
    def _filter_suitable_rooms(self, course, section, rooms):
        """Filter rooms suitable for the course and section."""
        suitable = []
        
        for room in rooms:
            # Check capacity
            if room.capacity < section.student_count:
                continue
            
            # Check room type for labs
            if course.course_type == 'lab' and room.room_type != 'lab':
                continue
            
            suitable.append(room)
        
        # Prioritize by capacity (prefer smaller rooms that fit)
        suitable.sort(key=lambda r: (r.capacity - section.student_count))
        
        return suitable
    
    def _filter_available_slots(self, teacher, all_slots):
        """Filter slots where teacher is available."""
        return [slot for slot in all_slots if teacher.is_available(slot)]
    
    def optimize_timetable(self, assignments):
        """
        Optimize existing timetable by reducing gaps and improving distribution.
        This is a simple local search optimization.
        """
        # This is a placeholder for future optimization algorithms
        # Could implement hill climbing, simulated annealing, or genetic algorithms
        print("Optimization not yet implemented - using initial solution")
        return assignments
