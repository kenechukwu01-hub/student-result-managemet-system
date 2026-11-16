"""Score entry, calculation and grading functions."""
from datetime import datetime

SUBJECTS = ["Mathematics", "English", "Physics", "Chemistry", "Biology"]


def calculate_grade(average):
    """Return a grade using the assignment's example grading scale."""
    if not 0 <= average <= 100:
        raise ValueError("Average must be between 0 and 100.")
    if average >= 70:
        return "A"
    if average >= 60:
        return "B"
    if average >= 50:
        return "C"
    if average >= 45:
        return "D"
    return "F"


def record_or_update_scores(student):
    """Collect at least five subject scores; existing scores can be replaced."""
    print("Subjects: " + ", ".join(SUBJECTS))
    updated = {}
    for subject in SUBJECTS:
        while True:
            raw = input(f"{subject} score: ").strip()
            try:
                score = float(raw)
                if not 0 <= score <= 100:
                    print("Score must be between 0 and 100.")
                    continue
                updated[subject] = score
                break
            except ValueError:
                print("Enter a valid number, for example 76 or 82.5.")
    student.scores = updated
    student.result_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
