# Smart Campus Management System

A simple web application to manage everyday campus activities: student records, daily attendance, room booking, and a notice board.

## Problem Statement and Objectives
Many small departments still track students, attendance, room usage and announcements in separate registers or spreadsheets, which causes double bookings, lost records and missed notices.

Objectives:
- Keep student records in one place.
- Record daily attendance and compute attendance percentages.
- Let staff book rooms without time-slot clashes.
- Share announcements on a notice board.

## Features / Modules Implemented
| Module | What it does |
|---|---|
| Students | Add, list and delete students (unique register number, email validation) |
| Attendance | Mark Present/Absent per date, edit a past date, view percentage report (below 75% highlighted) |
| Room Booking | Book rooms by date and time; overlapping bookings are rejected; cancel bookings |
| Notices | Post and delete notices; latest three shown on the dashboard |
| Dashboard | Summary counts and latest notices |

## Technology Stack and Tools
- Python 3.10+
- Flask (web framework), SQLite (database, built into Python)
- HTML/CSS with Jinja2 templates
- pytest (testing)
- Git and GitHub (version control)

## Prerequisites and Installation
1. Install Python 3.10 or newer and Git.
2. Clone the repository:
   ```
   git clone <your-repo-url>
   cd smart-campus
   ```
3. (Recommended) create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application
```
python app.py
```
Open http://127.0.0.1:5000 in a browser. The SQLite database (`campus.db`) is created automatically on first run, with three default rooms.

## Sample Inputs and Outputs
| Action | Input | Output |
|---|---|---|
| Add student | `CS101`, Asha, CSE, asha@example.com | "Student added." |
| Add student (bad email) | email = `asha` | "Enter a valid email address." |
| Duplicate register no. | `CS101` again | "A student with this register number already exists." |
| Book room | Lab 1, 2025-02-01, 10:00-11:00 | "Room booked." |
| Overlapping booking | Lab 1, 2025-02-01, 10:30-11:30 | "That room is already booked during this time slot." |
| Attendance report | 1 Present, 1 Absent | 50.0% (highlighted as below 75%) |

## Testing Performed and Results
Automated tests are in `tests/test_app.py`. Run them with:
```
python -m pytest -v
```
Covered: dashboard loading, student validation and duplicates, attendance saving and percentage calculation, invalid date handling, booking success, overlap rejection, back-to-back bookings allowed, invalid time range, notice posting and validation.

Result: 11 tests passed.

## Team Member Details and Contributions
| Name | Register No. | Contribution |
|---|---|---|
| _Your name_ | _Your reg. no._ | _e.g. whole project / modules built_ |

(Add one row per team member if this is a team project.)

## Known Limitations and Future Enhancements
Limitations:
- No login or user roles; anyone can use every feature.
- Single campus, single database file.
- No pagination or search on long lists.

Future enhancements:
- Staff / student / admin login with roles
- Export attendance report to CSV
- Search and filter students
- Email notifications for notices and bookings

## Acknowledgements
Built with [Flask](https://flask.palletsprojects.com/) and [pytest](https://pytest.org/).
## Git Workflow
The project is maintained using Git and GitHub.
A feature branch is used for changes before merging them into the main branch.
