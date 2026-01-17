"""
Utilities for data import/export and timetable formatting.
"""

import json
import csv
from models import Course, Teacher, Room, Section, TimeSlot


class DataLoader:
    """Load data from JSON or CSV files."""
    
    @staticmethod
    def load_courses_from_json(filepath):
        """Load courses from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        courses = []
        for item in data:
            course = Course(
                course_id=item['course_id'],
                name=item['name'],
                department=item['department'],
                hours_per_week=item['hours_per_week'],
                course_type=item.get('course_type', 'theory')
            )
            courses.append(course)
        return courses
    
    @staticmethod
    def load_teachers_from_json(filepath):
        """Load teachers from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        teachers = []
        for item in data:
            teacher = Teacher(
                teacher_id=item['teacher_id'],
                name=item['name'],
                department=item['department'],
                specializations=item.get('specializations', [])
            )
            
            # Load unavailable slots if specified
            if 'unavailable_slots' in item:
                for slot_data in item['unavailable_slots']:
                    slot = TimeSlot(
                        slot_data['day'],
                        slot_data['period'],
                        slot_data.get('start_time', ''),
                        slot_data.get('end_time', '')
                    )
                    teacher.add_unavailable_slot(slot)
            
            teachers.append(teacher)
        return teachers
    
    @staticmethod
    def load_rooms_from_json(filepath):
        """Load rooms from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        rooms = []
        for item in data:
            room = Room(
                room_id=item['room_id'],
                name=item['name'],
                capacity=item['capacity'],
                room_type=item.get('room_type', 'classroom')
            )
            rooms.append(room)
        return rooms
    
    @staticmethod
    def load_sections_from_json(filepath):
        """Load sections from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        sections = []
        for item in data:
            section = Section(
                section_id=item['section_id'],
                name=item['name'],
                department=item['department'],
                semester=item['semester'],
                student_count=item['student_count']
            )
            sections.append(section)
        return sections
    
    @staticmethod
    def load_course_assignments_from_json(filepath):
        """Load course-section-teacher assignments from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        assignments = {}
        for item in data:
            key = (item['course_id'], item['section_id'])
            assignments[key] = item['teacher_id']
        return assignments


class TimetableFormatter:
    """Format timetable for display and export."""
    
    @staticmethod
    def format_as_text(assignments, group_by='section'):
        """
        Format timetable as readable text.
        
        Args:
            assignments: List of ClassAssignment objects
            group_by: 'section', 'teacher', or 'room'
        """
        if not assignments:
            return "No assignments to display"
        
        lines = []
        lines.append("\n" + "="*80)
        lines.append("TIMETABLE - GLA UNIVERSITY")
        lines.append("="*80 + "\n")
        
        if group_by == 'section':
            grouped = TimetableFormatter._group_by_section(assignments)
            for section, classes in sorted(grouped.items()):
                lines.append(f"\n{section}")
                lines.append("-" * 80)
                for cls in sorted(classes, key=lambda x: (x.time_slot.day, x.time_slot.period)):
                    lines.append(
                        f"{cls.time_slot.day:12} | Period {cls.time_slot.period} "
                        f"({cls.time_slot.start_time}-{cls.time_slot.end_time}) | "
                        f"{cls.course.name:30} | {cls.teacher.name:20} | {cls.room.name}"
                    )
        
        elif group_by == 'teacher':
            grouped = TimetableFormatter._group_by_teacher(assignments)
            for teacher, classes in sorted(grouped.items()):
                lines.append(f"\n{teacher}")
                lines.append("-" * 80)
                for cls in sorted(classes, key=lambda x: (x.time_slot.day, x.time_slot.period)):
                    lines.append(
                        f"{cls.time_slot.day:12} | Period {cls.time_slot.period} "
                        f"({cls.time_slot.start_time}-{cls.time_slot.end_time}) | "
                        f"{cls.course.name:30} | {cls.section.name:15} | {cls.room.name}"
                    )
        
        elif group_by == 'room':
            grouped = TimetableFormatter._group_by_room(assignments)
            for room, classes in sorted(grouped.items()):
                lines.append(f"\n{room}")
                lines.append("-" * 80)
                for cls in sorted(classes, key=lambda x: (x.time_slot.day, x.time_slot.period)):
                    lines.append(
                        f"{cls.time_slot.day:12} | Period {cls.time_slot.period} "
                        f"({cls.time_slot.start_time}-{cls.time_slot.end_time}) | "
                        f"{cls.course.name:30} | {cls.section.name:15} | {cls.teacher.name}"
                    )
        
        return "\n".join(lines)
    
    @staticmethod
    def export_to_csv(assignments, filepath):
        """Export timetable to CSV file."""
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Day', 'Period', 'Start Time', 'End Time',
                'Course ID', 'Course Name', 'Section', 'Teacher', 'Room'
            ])
            
            for assignment in sorted(assignments, 
                                   key=lambda x: (x.time_slot.day, x.time_slot.period)):
                writer.writerow([
                    assignment.time_slot.day,
                    assignment.time_slot.period,
                    assignment.time_slot.start_time,
                    assignment.time_slot.end_time,
                    assignment.course.course_id,
                    assignment.course.name,
                    assignment.section.name,
                    assignment.teacher.name,
                    assignment.room.name
                ])
        
        print(f"Timetable exported to {filepath}")
    
    @staticmethod
    def export_to_json(assignments, filepath):
        """Export timetable to JSON file."""
        data = []
        for assignment in assignments:
            data.append({
                'day': assignment.time_slot.day,
                'period': assignment.time_slot.period,
                'start_time': assignment.time_slot.start_time,
                'end_time': assignment.time_slot.end_time,
                'course_id': assignment.course.course_id,
                'course_name': assignment.course.name,
                'section_id': assignment.section.section_id,
                'section_name': assignment.section.name,
                'teacher_id': assignment.teacher.teacher_id,
                'teacher_name': assignment.teacher.name,
                'room_id': assignment.room.room_id,
                'room_name': assignment.room.name
            })
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Timetable exported to {filepath}")
    
    @staticmethod
    def _group_by_section(assignments):
        """Group assignments by section."""
        grouped = {}
        for assignment in assignments:
            key = str(assignment.section)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(assignment)
        return grouped
    
    @staticmethod
    def _group_by_teacher(assignments):
        """Group assignments by teacher."""
        grouped = {}
        for assignment in assignments:
            key = str(assignment.teacher)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(assignment)
        return grouped
    
    @staticmethod
    def _group_by_room(assignments):
        """Group assignments by room."""
        grouped = {}
        for assignment in assignments:
            key = str(assignment.room)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(assignment)
        return grouped
