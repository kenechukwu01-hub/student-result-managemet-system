"""Functions for displaying and saving student and class reports."""
from datetime import datetime
import os


def student_report_text(student):
    lines = [
        "=" * 55,
        "             STUDENT ACADEMIC REPORT CARD",
        "=" * 55,
        f"Student ID     : {student.student_id}",
        f"Full Name      : {student.full_name}",
        f"Class/Form     : {student.class_form}",
        f"Gender         : {student.gender}",
        f"Date of Birth  : {student.date_of_birth}",
        "-" * 55,
        f"{'SUBJECT':<25}{'SCORE':>10}",
        "-" * 55
    ]
    for subject, score in student.scores.items():
        lines.append(f"{subject:<25}{float(score):>10.2f}")
    if student.scores:
        lines.extend([
            "-" * 55,
            f"{'TOTAL':<25}{student.total:>10.2f}",
            f"{'AVERAGE':<25}{student.average:>10.2f}",
            f"{'GRADE':<25}{student.grade:>10}",
            f"Result entered: {student.result_date or 'Not recorded'}"
        ])
    else:
        lines.append("No examination scores have been entered.")
    lines.append("=" * 55)
    return "\n".join(lines)


def display_student_report(student):
    print(student_report_text(student))


def display_all_results(students):
    if not students:
        print("No student records available.")
        return
    ranked = sorted(students, key=lambda s: s.average, reverse=True)
    print(f"\n{'RANK':<6}{'STUDENT ID':<15}{'NAME':<25}{'TOTAL':>9}{'AVERAGE':>11}{'GRADE':>8}")
    print("-" * 74)
    for rank, student in enumerate(ranked, start=1):
        grade = student.grade
        print(f"{rank:<6}{student.student_id:<15}{student.full_name[:24]:<25}"
              f"{student.total:>9.2f}{student.average:>11.2f}{grade:>8}")


def class_statistics(students):
    assessed = [s for s in students if s.scores]
    if not assessed:
        return None
    highest = max(assessed, key=lambda s: s.average)
    lowest = min(assessed, key=lambda s: s.average)
    class_average = sum(s.average for s in assessed) / len(assessed)
    return {
        "assessed_count": len(assessed),
        "highest": highest,
        "lowest": lowest,
        "class_average": class_average
    }


def display_class_statistics(students):
    stats = class_statistics(students)
    if stats is None:
        print("There are no students with recorded scores yet.")
        return
    print("\n--- CLASS STATISTICS ---")
    print(f"Students with results: {stats['assessed_count']}")
    print(f"Highest average: {stats['highest'].average:.2f} - {stats['highest'].full_name}")
    print(f"Lowest average : {stats['lowest'].average:.2f} - {stats['lowest'].full_name}")
    print(f"Class average  : {stats['class_average']:.2f}")


def save_student_report(student):
    os.makedirs("reports", exist_ok=True)
    safe_id = "".join(c for c in student.student_id if c.isalnum() or c in "-_")
    path = os.path.join("reports", f"{safe_id}_report.txt")
    with open(path, "w", encoding="utf-8") as file:
        file.write(student_report_text(student))
    return path


def save_class_report(students):
    os.makedirs("reports", exist_ok=True)
    path = os.path.join("reports", f"class_report_{datetime.now():%Y%m%d_%H%M%S}.txt")
    lines = ["STUDENT RESULT MANAGEMENT SYSTEM - CLASS REPORT",
             f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}", ""]
    for student in sorted(students, key=lambda s: s.average, reverse=True):
        lines.append(f"{student.student_id} | {student.full_name} | "
                     f"Total: {student.total:.2f} | Average: {student.average:.2f} | "
                     f"Grade: {student.grade}")
    stats = class_statistics(students)
    if stats:
        lines.extend(["", f"Students assessed: {stats['assessed_count']}",
                      f"Highest average: {stats['highest'].average:.2f} "
                      f"({stats['highest'].full_name})",
                      f"Lowest average: {stats['lowest'].average:.2f} "
                      f"({stats['lowest'].full_name})",
                      f"Class average: {stats['class_average']:.2f}"])
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    return path
