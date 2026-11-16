# Student Result Management System

## Project description
A menu-driven Python application for registering students, recording examination scores in five subjects, calculating totals, averages and grades, displaying report cards, ranking students, and producing class statistics.

## Features
- Register, view, search, update and delete student records.
- Record or update scores in Mathematics, English, Physics, Chemistry and Biology.
- Calculate total score, average and grade automatically.
- Display individual report cards and rank students by average.
- Calculate highest average, lowest average and class average.
- Save individual and class reports as text files.
- Store student information persistently in `data/students.json`.
- Validate dates and scores and handle common file/input errors.

## Requirements
- Python 3.9 or later.
- No third-party packages are required; the project uses the Python standard library.

## How to run
1. Download or clone this repository.
2. Open a terminal in the `student_result_system` folder.
3. Run:

   ```bash
   python main.py
   ```

   On some Windows installations, use `py main.py`.

4. Select an option from the menu and follow the prompts.

## Grading scale
| Average score | Grade |
|---|---|
| 70–100 | A |
| 60–69.99 | B |
| 50–59.99 | C |
| 45–49.99 | D |
| 0–44.99 | F |

This follows the example grading scale in the project brief.

## Project structure
```text
student_result_system/
├── main.py
├── student.py
├── results.py
├── storage.py
├── reports.py
├── data/
│   └── students.json
├── reports/             # Generated report files appear here
└── README.md
```

## Python concepts demonstrated
- Variables, strings, numbers, dictionaries and lists.
- Conditional statements and loops.
- Functions with parameters and return values.
- Object-oriented programming through the `Student` class.
- Sorting using `sorted()` and a key function.
- Exception handling with `try` and `except`.
- JSON file reading and writing.
- Modules and imports.
- Date and time handling with `datetime`.
- File and folder operations using `os`.

## Notes
- Student IDs must be unique.
- Scores must be numeric and between 0 and 100.
- A student's average is calculated from the subjects with recorded scores.
- The application begins with an empty student list if the JSON data file does not exist.
