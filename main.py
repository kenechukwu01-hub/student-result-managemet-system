"""Entry point for the Student Result Management System."""
from student import Student
from storage import load_students, save_students
from results import record_or_update_scores
from reports import (
    display_student_report, display_all_results, display_class_statistics,
    save_student_report, save_class_report
)

DATA_FILE = "data/students.json"


def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def find_student(students):
    key = input("Enter student ID or full name: ").strip().lower()
    for student in students:
        if student.student_id.lower() == key or student.full_name.lower() == key:
            return student
    print("Student not found.")
    return None


def add_student(students):
    print("\n--- Register Student ---")
    student_id = read_non_empty("Student ID: ")
    if any(s.student_id.lower() == student_id.lower() for s in students):
        print("A student with that ID already exists.")
        return
    full_name = read_non_empty("Full name: ")
    class_form = read_non_empty("Class/Form: ")
    gender = read_non_empty("Gender: ")
    dob = read_non_empty("Date of birth (YYYY-MM-DD): ")
    try:
        student = Student(student_id, full_name, class_form, gender, dob)
        students.append(student)
        save_students(students, DATA_FILE)
        print("Student registered successfully.")
    except ValueError as error:
        print(f"Invalid information: {error}")


def view_students(students):
    if not students:
        print("No students have been registered.")
        return
    print("\n--- Registered Students ---")
    for s in sorted(students, key=lambda item: item.full_name.lower()):
        print(f"{s.student_id:<15} {s.full_name:<28} {s.class_form:<15} {s.gender}")


def update_student(students):
    student = find_student(students)
    if not student:
        return
    print("Press Enter to keep the current value.")
    name = input(f"Full name [{student.full_name}]: ").strip() or student.full_name
    class_form = input(f"Class/Form [{student.class_form}]: ").strip() or student.class_form
    gender = input(f"Gender [{student.gender}]: ").strip() or student.gender
    dob = input(f"Date of birth [{student.date_of_birth}]: ").strip() or student.date_of_birth
    try:
        student.update_details(name, class_form, gender, dob)
        save_students(students, DATA_FILE)
        print("Student information updated.")
    except ValueError as error:
        print(f"Update failed: {error}")


def delete_student(students):
    student = find_student(students)
    if not student:
        return
    confirm = input(f"Delete {student.full_name}? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students(students, DATA_FILE)
        print("Student record deleted.")


def enter_scores(students):
    student = find_student(students)
    if not student:
        return
    print("Enter a score from 0 to 100 for each subject.")
    try:
        record_or_update_scores(student)
        save_students(students, DATA_FILE)
        print("Scores saved successfully.")
    except ValueError as error:
        print(f"Could not save scores: {error}")


def show_student_report(students):
    student = find_student(students)
    if student:
        display_student_report(student)
        if input("Save this report to a text file? (y/n): ").strip().lower() == "y":
            path = save_student_report(student)
            print(f"Report saved to: {path}")


def menu():
    print("""
========== STUDENT RESULT MANAGEMENT SYSTEM ==========
1. Register a new student
2. View all students
3. Search for a student
4. Update student information
5. Delete a student
6. Record or update subject scores
7. View an individual report card
8. View all students' results (sorted by average)
9. View class statistics
10. Save class report to a text file
0. Exit
======================================================
""")


def main():
    students = load_students(DATA_FILE)
    print(f"Welcome! {len(students)} student record(s) loaded.")
    while True:
        menu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            student = find_student(students)
            if student:
                print(student)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            enter_scores(students)
        elif choice == "7":
            show_student_report(students)
        elif choice == "8":
            display_all_results(students)
        elif choice == "9":
            display_class_statistics(students)
        elif choice == "10":
            path = save_class_report(students)
            print(f"Class report saved to: {path}")
        elif choice == "0":
            save_students(students, DATA_FILE)
            print("All records saved. Goodbye!")
            break
        else:
            print("Invalid option. Choose a number from 0 to 10.")


if __name__ == "__main__":
    main()
