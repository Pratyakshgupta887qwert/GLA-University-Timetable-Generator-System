#!/usr/bin/env python3
"""
GLA University Timetable Generator System
Main command-line interface for timetable generation.
"""

import sys
import argparse
from pathlib import Path

from config import TimetableConfig
from generator import TimetableGenerator
from utils import DataLoader, TimetableFormatter
from constraints import ConflictDetector


def main():
    """Main entry point for the timetable generator."""
    parser = argparse.ArgumentParser(
        description='GLA University Timetable Generator System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate timetable with sample data
  python main.py --sample
  
  # Generate timetable from custom data files
  python main.py --courses data/courses.json --teachers data/teachers.json \\
                 --rooms data/rooms.json --sections data/sections.json \\
                 --assignments data/assignments.json
  
  # Export timetable to CSV
  python main.py --sample --export-csv output/timetable.csv
  
  # View timetable grouped by teacher
  python main.py --sample --group-by teacher
        """
    )
    
    # Input data arguments
    parser.add_argument('--courses', help='Path to courses JSON file')
    parser.add_argument('--teachers', help='Path to teachers JSON file')
    parser.add_argument('--rooms', help='Path to rooms JSON file')
    parser.add_argument('--sections', help='Path to sections JSON file')
    parser.add_argument('--assignments', help='Path to course assignments JSON file')
    parser.add_argument('--config', help='Path to configuration JSON file')
    
    # Sample data option
    parser.add_argument('--sample', action='store_true',
                       help='Use sample data for demonstration')
    
    # Output options
    parser.add_argument('--export-csv', help='Export timetable to CSV file')
    parser.add_argument('--export-json', help='Export timetable to JSON file')
    parser.add_argument('--group-by', choices=['section', 'teacher', 'room'],
                       default='section', help='Group timetable display by (default: section)')
    
    # Generation options
    parser.add_argument('--max-attempts', type=int, default=10000,
                       help='Maximum scheduling attempts (default: 10000)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    # Set random seed if specified
    if args.seed:
        import random
        random.seed(args.seed)
        print(f"Using random seed: {args.seed}")
    
    print("\n" + "="*80)
    print("GLA UNIVERSITY TIMETABLE GENERATOR SYSTEM")
    print("="*80 + "\n")
    
    # Load configuration
    config = TimetableConfig()
    if args.config:
        print(f"Loading configuration from {args.config}...")
        if config.load_from_file(args.config):
            print("✓ Configuration loaded successfully")
        else:
            print("✗ Failed to load configuration, using defaults")
    else:
        print("Using default configuration")
    
    print(f"Configuration: {config}\n")
    
    # Load data
    if args.sample:
        print("Using sample data...")
        courses, teachers, rooms, sections, course_assignments = create_sample_data()
    else:
        if not all([args.courses, args.teachers, args.rooms, args.sections, args.assignments]):
            print("Error: When not using --sample, all data files must be specified:")
            print("  --courses, --teachers, --rooms, --sections, --assignments")
            sys.exit(1)
        
        print("Loading data from files...")
        try:
            courses = DataLoader.load_courses_from_json(args.courses)
            teachers = DataLoader.load_teachers_from_json(args.teachers)
            rooms = DataLoader.load_rooms_from_json(args.rooms)
            sections = DataLoader.load_sections_from_json(args.sections)
            course_assignments = DataLoader.load_course_assignments_from_json(args.assignments)
            print("✓ All data loaded successfully")
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            sys.exit(1)
    
    print(f"\nData Summary:")
    print(f"  Courses: {len(courses)}")
    print(f"  Teachers: {len(teachers)}")
    print(f"  Rooms: {len(rooms)}")
    print(f"  Sections: {len(sections)}")
    print(f"  Course Assignments: {len(course_assignments)}")
    
    # Generate timetable
    print("\n" + "-"*80)
    generator = TimetableGenerator(config)
    timetable = generator.generate(
        courses, sections, teachers, rooms, course_assignments
    )
    
    if timetable is None:
        print("\n✗ Failed to generate a valid timetable")
        print("Try:")
        print("  - Adding more rooms")
        print("  - Adding more time slots")
        print("  - Reducing course hours")
        print("  - Checking teacher availability constraints")
        sys.exit(1)
    
    # Check for conflicts
    print("\nValidating timetable...")
    conflicts = ConflictDetector.find_all_conflicts(timetable)
    conflict_count = ConflictDetector.count_conflicts(conflicts)
    
    if conflict_count > 0:
        print(ConflictDetector.format_conflict_report(conflicts))
    else:
        print("✓ Timetable validation passed - no conflicts detected!")
    
    # Display timetable
    print("\n" + "-"*80)
    print(TimetableFormatter.format_as_text(timetable, group_by=args.group_by))
    
    # Export if requested
    if args.export_csv:
        Path(args.export_csv).parent.mkdir(parents=True, exist_ok=True)
        TimetableFormatter.export_to_csv(timetable, args.export_csv)
    
    if args.export_json:
        Path(args.export_json).parent.mkdir(parents=True, exist_ok=True)
        TimetableFormatter.export_to_json(timetable, args.export_json)
    
    print("\n" + "="*80)
    print("Timetable generation completed successfully!")
    print("="*80 + "\n")


def create_sample_data():
    """Create sample data for demonstration."""
    from models import Course, Teacher, Room, Section, TimeSlot
    
    # Sample courses
    courses = [
        Course("CS101", "Data Structures", "Computer Science", 3, "theory"),
        Course("CS102", "Algorithms", "Computer Science", 3, "theory"),
        Course("CS103", "Database Systems", "Computer Science", 3, "theory"),
        Course("CS104", "Programming Lab", "Computer Science", 2, "lab"),
        Course("MA101", "Calculus I", "Mathematics", 4, "theory"),
        Course("MA102", "Linear Algebra", "Mathematics", 3, "theory"),
        Course("PH101", "Physics I", "Physics", 3, "theory"),
        Course("PH102", "Physics Lab", "Physics", 2, "lab"),
    ]
    
    # Sample teachers
    teachers = [
        Teacher("T001", "Dr. Sharma", "Computer Science", ["Data Structures", "Algorithms"]),
        Teacher("T002", "Dr. Patel", "Computer Science", ["Database", "Programming"]),
        Teacher("T003", "Dr. Kumar", "Computer Science", ["Programming", "Software Engineering"]),
        Teacher("T004", "Dr. Singh", "Mathematics", ["Calculus", "Algebra"]),
        Teacher("T005", "Dr. Gupta", "Mathematics", ["Linear Algebra", "Statistics"]),
        Teacher("T006", "Dr. Verma", "Physics", ["Mechanics", "Thermodynamics"]),
    ]
    
    # Add some unavailable slots for Dr. Sharma (meetings on Monday period 1 and Friday period 6)
    teachers[0].add_unavailable_slot(TimeSlot("Monday", 1, "09:00", "10:00"))
    teachers[0].add_unavailable_slot(TimeSlot("Friday", 6, "15:00", "16:00"))
    
    # Sample rooms
    rooms = [
        Room("R001", "Room 101", 60, "classroom"),
        Room("R002", "Room 102", 60, "classroom"),
        Room("R003", "Room 103", 50, "classroom"),
        Room("R004", "Room 104", 50, "classroom"),
        Room("R005", "Room 105", 40, "classroom"),
        Room("L001", "Lab 201", 60, "lab"),
        Room("L002", "Lab 202", 60, "lab"),
    ]
    
    # Sample sections
    sections = [
        Section("S001", "CS-A", "Computer Science", 3, 55),
        Section("S002", "CS-B", "Computer Science", 3, 50),
        Section("S003", "MA-A", "Mathematics", 3, 45),
    ]
    
    # Course assignments (which teacher teaches which course to which section)
    course_assignments = {
        ("CS101", "S001"): "T001",
        ("CS101", "S002"): "T001",
        ("CS102", "S001"): "T002",
        ("CS102", "S002"): "T002",
        ("CS103", "S001"): "T003",
        ("CS103", "S002"): "T003",
        ("CS104", "S001"): "T002",
        ("CS104", "S002"): "T003",
        ("MA101", "S001"): "T004",
        ("MA101", "S002"): "T004",
        ("MA101", "S003"): "T004",
        ("MA102", "S003"): "T005",
        ("PH101", "S001"): "T006",
        ("PH102", "S001"): "T006",
    }
    
    return courses, teachers, rooms, sections, course_assignments


if __name__ == "__main__":
    main()
