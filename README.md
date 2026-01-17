# GLA University Timetable Generator System

An intelligent, automated timetable generation system designed to simplify and optimize academic scheduling for educational institutions. This system employs constraint-based algorithms to ensure conflict-free scheduling while maximizing resource utilization and meeting institution-specific requirements.

## 🌟 Key Features

- **Conflict-Free Scheduling**: Advanced constraint validation ensures no teacher, room, or section double-booking
- **Smart Algorithms**: Constraint satisfaction with backtracking for optimal schedule generation
- **Institution-Specific Rules**: Fully customizable configuration for different institutional requirements
- **Resource Management**: Efficient handling of classes, staff, rooms, and time slots
- **Comprehensive Validation**: Detailed conflict detection and reporting
- **Multiple Export Formats**: Output timetables in CSV, JSON, or formatted text
- **Flexible Viewing**: Group timetables by section, teacher, or room
- **Lab Support**: Specialized handling for laboratory courses and room types
- **Teacher Availability**: Respect faculty unavailability constraints
- **Capacity Management**: Automatic room capacity validation

## 📋 Requirements

- Python 3.7 or higher
- pandas >= 1.5.0
- numpy >= 1.23.0

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Pratyakshgupta887qwert/GLA-University-Timetable-Generator-System.git
cd GLA-University-Timetable-Generator-System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

Generate a timetable with sample data:
```bash
python main.py --sample
```

Generate and export to CSV:
```bash
python main.py --sample --export-csv output/timetable.csv
```

View timetable grouped by teacher:
```bash
python main.py --sample --group-by teacher
```

## 📖 Detailed Usage

### Using Custom Data

Prepare your data files in JSON format (see `examples/` directory for templates):

```bash
python main.py \
  --courses examples/courses.json \
  --teachers examples/teachers.json \
  --rooms examples/rooms.json \
  --sections examples/sections.json \
  --assignments examples/assignments.json
```

### Configuration

Create a custom configuration file:

```bash
python main.py --sample --config examples/config.json
```

Configuration options include:
- Working days and time slots
- Maximum classes per day
- Consecutive class limits
- Room type requirements
- Optimization weights

### Command-Line Options

```
--sample                Use built-in sample data
--courses FILE         Path to courses JSON file
--teachers FILE        Path to teachers JSON file
--rooms FILE           Path to rooms JSON file
--sections FILE        Path to sections JSON file
--assignments FILE     Path to course assignments JSON file
--config FILE          Path to configuration JSON file
--export-csv FILE      Export timetable to CSV
--export-json FILE     Export timetable to JSON
--group-by TYPE        Group by: section, teacher, or room
--max-attempts N       Maximum scheduling attempts
--seed N               Random seed for reproducibility
```

## 📁 Data Format

### Courses (courses.json)
```json
[
  {
    "course_id": "CS101",
    "name": "Data Structures",
    "department": "Computer Science",
    "hours_per_week": 3,
    "course_type": "theory"
  }
]
```

### Teachers (teachers.json)
```json
[
  {
    "teacher_id": "T001",
    "name": "Dr. Sharma",
    "department": "Computer Science",
    "specializations": ["Data Structures", "Algorithms"],
    "unavailable_slots": [
      {"day": "Monday", "period": 1, "start_time": "09:00", "end_time": "10:00"}
    ]
  }
]
```

### Rooms (rooms.json)
```json
[
  {
    "room_id": "R001",
    "name": "Room 101",
    "capacity": 60,
    "room_type": "classroom"
  }
]
```

### Sections (sections.json)
```json
[
  {
    "section_id": "S001",
    "name": "CS-A",
    "department": "Computer Science",
    "semester": 3,
    "student_count": 55
  }
]
```

### Assignments (assignments.json)
```json
[
  {
    "course_id": "CS101",
    "section_id": "S001",
    "teacher_id": "T001"
  }
]
```

## 🏗️ Architecture

### Core Components

1. **models.py**: Data models for courses, teachers, rooms, sections, and assignments
2. **constraints.py**: Constraint validation and conflict detection
3. **generator.py**: Main timetable generation engine with backtracking algorithm
4. **config.py**: Configuration management for institution-specific rules
5. **utils.py**: Data I/O and timetable formatting utilities
6. **main.py**: Command-line interface

### Algorithm

The system uses a **constraint satisfaction problem (CSP)** approach with backtracking:

1. **Request Prioritization**: Lab courses and high-hour courses scheduled first
2. **Constraint Checking**: Validates teacher, room, and section availability
3. **Backtracking**: Recursively explores schedule space, backtracking on conflicts
4. **Validation**: Post-generation conflict detection ensures validity

### Constraints Enforced

- ✓ No teacher double-booking
- ✓ No room double-booking
- ✓ No section schedule conflicts
- ✓ Room capacity requirements
- ✓ Teacher availability preferences
- ✓ Lab courses require lab rooms
- ✓ Configurable institutional rules

## 📊 Example Output

```
================================================================================
TIMETABLE - GLA UNIVERSITY
================================================================================

CS-A (Sem 3)
--------------------------------------------------------------------------------
Monday       | Period 2 (10:00-11:00) | Data Structures                | Dr. Sharma           | Room 101
Monday       | Period 3 (11:00-12:00) | Algorithms                     | Dr. Patel            | Room 102
Tuesday      | Period 1 (09:00-10:00) | Database Systems               | Dr. Kumar            | Room 103
...
```

## 🔧 Customization

### Adding New Constraints

Extend the `ConstraintValidator` class in `constraints.py`:

```python
def _check_custom_constraint(self, assignment, existing_assignments):
    # Your constraint logic here
    pass
```

### Modifying Scheduling Algorithm

The backtracking algorithm in `generator.py` can be enhanced with:
- Heuristic ordering strategies
- Constraint propagation techniques
- Local search optimization
- Genetic algorithms

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

GLA University Timetable Generator System Development Team

## 🙏 Acknowledgments

- Inspired by constraint satisfaction problem algorithms
- Built for educational institutions seeking efficient scheduling solutions

## 📞 Support

For questions or support, please open an issue on the GitHub repository.

---

**Note**: This system is designed to be adaptable to various educational institutions. Customize the configuration and data formats to match your specific requirements.
