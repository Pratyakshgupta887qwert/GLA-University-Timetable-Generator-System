"""
Constraint validation and conflict detection for timetable generation.
"""

class ConstraintValidator:
    """Validates scheduling constraints and detects conflicts."""
    
    def __init__(self):
        self.conflicts = []
    
    def validate_assignment(self, assignment, existing_assignments):
        """
        Validate a class assignment against all constraints.
        Returns (is_valid, conflicts_list)
        """
        self.conflicts = []
        
        # Check all constraints
        self._check_teacher_conflict(assignment, existing_assignments)
        self._check_room_conflict(assignment, existing_assignments)
        self._check_section_conflict(assignment, existing_assignments)
        self._check_room_capacity(assignment)
        self._check_teacher_availability(assignment)
        self._check_room_type_compatibility(assignment)
        
        return len(self.conflicts) == 0, self.conflicts
    
    def _check_teacher_conflict(self, assignment, existing_assignments):
        """Ensure teacher is not double-booked."""
        for existing in existing_assignments:
            if (existing.teacher == assignment.teacher and 
                existing.time_slot == assignment.time_slot):
                self.conflicts.append(
                    f"Teacher conflict: {assignment.teacher.name} is already "
                    f"scheduled at {assignment.time_slot}"
                )
    
    def _check_room_conflict(self, assignment, existing_assignments):
        """Ensure room is not double-booked."""
        for existing in existing_assignments:
            if (existing.room == assignment.room and 
                existing.time_slot == assignment.time_slot):
                self.conflicts.append(
                    f"Room conflict: {assignment.room.name} is already "
                    f"occupied at {assignment.time_slot}"
                )
    
    def _check_section_conflict(self, assignment, existing_assignments):
        """Ensure section doesn't have overlapping classes."""
        for existing in existing_assignments:
            if (existing.section == assignment.section and 
                existing.time_slot == assignment.time_slot):
                self.conflicts.append(
                    f"Section conflict: {assignment.section.name} already has "
                    f"a class at {assignment.time_slot}"
                )
    
    def _check_room_capacity(self, assignment):
        """Ensure room has sufficient capacity for the section."""
        if assignment.room.capacity < assignment.section.student_count:
            self.conflicts.append(
                f"Capacity conflict: Room {assignment.room.name} "
                f"(capacity: {assignment.room.capacity}) is too small for "
                f"section {assignment.section.name} "
                f"(students: {assignment.section.student_count})"
            )
    
    def _check_teacher_availability(self, assignment):
        """Ensure teacher is available at the scheduled time."""
        if not assignment.teacher.is_available(assignment.time_slot):
            self.conflicts.append(
                f"Availability conflict: {assignment.teacher.name} is not "
                f"available at {assignment.time_slot}"
            )
    
    def _check_room_type_compatibility(self, assignment):
        """Ensure room type matches course requirements."""
        if assignment.course.course_type == "lab" and assignment.room.room_type != "lab":
            self.conflicts.append(
                f"Room type conflict: Course {assignment.course.name} requires "
                f"a lab but {assignment.room.name} is a {assignment.room.room_type}"
            )


class ConflictDetector:
    """Detects and reports conflicts in a complete timetable."""
    
    @staticmethod
    def find_all_conflicts(assignments):
        """
        Find all conflicts in a list of assignments.
        Returns a dictionary of conflict types and their details.
        """
        conflicts = {
            'teacher_conflicts': [],
            'room_conflicts': [],
            'section_conflicts': [],
            'capacity_issues': [],
            'availability_issues': [],
            'room_type_issues': []
        }
        
        # Build lookup dictionaries
        teacher_schedule = {}
        room_schedule = {}
        section_schedule = {}
        
        for assignment in assignments:
            key = assignment.time_slot
            
            # Track teacher schedules
            if assignment.teacher not in teacher_schedule:
                teacher_schedule[assignment.teacher] = {}
            if key in teacher_schedule[assignment.teacher]:
                conflicts['teacher_conflicts'].append({
                    'teacher': assignment.teacher.name,
                    'time_slot': str(key),
                    'courses': [
                        teacher_schedule[assignment.teacher][key].course.name,
                        assignment.course.name
                    ]
                })
            teacher_schedule[assignment.teacher][key] = assignment
            
            # Track room schedules
            if assignment.room not in room_schedule:
                room_schedule[assignment.room] = {}
            if key in room_schedule[assignment.room]:
                conflicts['room_conflicts'].append({
                    'room': assignment.room.name,
                    'time_slot': str(key),
                    'courses': [
                        room_schedule[assignment.room][key].course.name,
                        assignment.course.name
                    ]
                })
            room_schedule[assignment.room][key] = assignment
            
            # Track section schedules
            if assignment.section not in section_schedule:
                section_schedule[assignment.section] = {}
            if key in section_schedule[assignment.section]:
                conflicts['section_conflicts'].append({
                    'section': assignment.section.name,
                    'time_slot': str(key),
                    'courses': [
                        section_schedule[assignment.section][key].course.name,
                        assignment.course.name
                    ]
                })
            section_schedule[assignment.section][key] = assignment
            
            # Check capacity
            if assignment.room.capacity < assignment.section.student_count:
                conflicts['capacity_issues'].append({
                    'room': assignment.room.name,
                    'capacity': assignment.room.capacity,
                    'section': assignment.section.name,
                    'student_count': assignment.section.student_count,
                    'time_slot': str(key)
                })
            
            # Check availability
            if not assignment.teacher.is_available(assignment.time_slot):
                conflicts['availability_issues'].append({
                    'teacher': assignment.teacher.name,
                    'time_slot': str(key)
                })
            
            # Check room type
            if (assignment.course.course_type == "lab" and 
                assignment.room.room_type != "lab"):
                conflicts['room_type_issues'].append({
                    'course': assignment.course.name,
                    'room': assignment.room.name,
                    'room_type': assignment.room.room_type,
                    'required_type': 'lab'
                })
        
        return conflicts
    
    @staticmethod
    def count_conflicts(conflicts):
        """Count total number of conflicts."""
        return sum(len(v) for v in conflicts.values())
    
    @staticmethod
    def format_conflict_report(conflicts):
        """Format conflicts into a readable report."""
        report = []
        total = ConflictDetector.count_conflicts(conflicts)
        
        report.append(f"\n=== Conflict Detection Report ===")
        report.append(f"Total conflicts found: {total}\n")
        
        if conflicts['teacher_conflicts']:
            report.append(f"Teacher Conflicts ({len(conflicts['teacher_conflicts'])}):")
            for c in conflicts['teacher_conflicts']:
                report.append(f"  - {c['teacher']} has overlapping classes at {c['time_slot']}")
                report.append(f"    Courses: {', '.join(c['courses'])}")
        
        if conflicts['room_conflicts']:
            report.append(f"\nRoom Conflicts ({len(conflicts['room_conflicts'])}):")
            for c in conflicts['room_conflicts']:
                report.append(f"  - {c['room']} is double-booked at {c['time_slot']}")
                report.append(f"    Courses: {', '.join(c['courses'])}")
        
        if conflicts['section_conflicts']:
            report.append(f"\nSection Conflicts ({len(conflicts['section_conflicts'])}):")
            for c in conflicts['section_conflicts']:
                report.append(f"  - {c['section']} has overlapping classes at {c['time_slot']}")
                report.append(f"    Courses: {', '.join(c['courses'])}")
        
        if conflicts['capacity_issues']:
            report.append(f"\nCapacity Issues ({len(conflicts['capacity_issues'])}):")
            for c in conflicts['capacity_issues']:
                report.append(f"  - Room {c['room']} (capacity: {c['capacity']}) is too small "
                            f"for section {c['section']} ({c['student_count']} students)")
        
        if conflicts['availability_issues']:
            report.append(f"\nAvailability Issues ({len(conflicts['availability_issues'])}):")
            for c in conflicts['availability_issues']:
                report.append(f"  - {c['teacher']} is not available at {c['time_slot']}")
        
        if conflicts['room_type_issues']:
            report.append(f"\nRoom Type Issues ({len(conflicts['room_type_issues'])}):")
            for c in conflicts['room_type_issues']:
                report.append(f"  - Course {c['course']} requires {c['required_type']} "
                            f"but assigned {c['room']} ({c['room_type']})")
        
        if total == 0:
            report.append("No conflicts detected! Timetable is valid.")
        
        return "\n".join(report)
