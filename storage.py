"""JSON data persistence functions."""
import json
import os
from student import Student


def load_students(file_path):
    """Load saved student records. Return an empty list if no file exists yet."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            records = json.load(file)
        return [Student.from_dict(record) for record in records]
    except json.JSONDecodeError as error:
        print(f"Warning: the data file is not valid JSON ({error}). Starting with no records.")
        return []
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"Warning: records could not be loaded ({error}). Starting with no records.")
        return []


def save_students(students, file_path):
    """Save all student records to JSON, creating the data folder if needed."""
    folder = os.path.dirname(file_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    temporary_path = file_path + ".tmp"
    try:
        with open(temporary_path, "w", encoding="utf-8") as file:
            json.dump([student.to_dict() for student in students], file, indent=4)
        os.replace(temporary_path, file_path)
    except OSError as error:
        print(f"Error saving records: {error}")
        if os.path.exists(temporary_path):
            os.remove(temporary_path)
