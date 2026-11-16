"""Flask web interface for the Student Result Management System."""
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from student import Student
from storage import load_students, save_students
from results import SUBJECTS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "development-key-change-before-production")
DATA_FILE = os.environ.get("DATA_FILE", "data/students.json")

def records():
    return load_students(DATA_FILE)

def find_student(student_id, students):
    for student in students:
        if student.student_id == student_id:
            return student
    abort(404)

@app.route("/")
def index():
    students = records()
    assessed = [s for s in students if s.scores]
    average = sum(s.average for s in assessed) / len(assessed) if assessed else 0
    highest = max(assessed, key=lambda s: s.average) if assessed else None
    return render_template("index.html", students=sorted(students, key=lambda s: s.full_name.lower()),
                           total=len(students), assessed=len(assessed), class_average=average, highest=highest)

@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        students = records()
        sid = request.form.get("student_id", "").strip()
        if any(s.student_id.lower() == sid.lower() for s in students):
            flash("That student ID is already registered.", "error")
            return render_template("student_form.html", student=None)
        try:
            student = Student(sid, request.form.get("full_name", ""), request.form.get("class_form", ""),
                              request.form.get("gender", ""), request.form.get("date_of_birth", ""))
            students.append(student)
            save_students(students, DATA_FILE)
            flash("Student registered successfully.", "success")
            return redirect(url_for("index"))
        except ValueError as exc:
            flash(str(exc), "error")
    return render_template("student_form.html", student=None)

@app.route("/students/<student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    students = records()
    student = find_student(student_id, students)
    if request.method == "POST":
        try:
            student.update_details(request.form.get("full_name", ""), request.form.get("class_form", ""),
                                   request.form.get("gender", ""), request.form.get("date_of_birth", ""))
            save_students(students, DATA_FILE)
            flash("Student details updated.", "success")
            return redirect(url_for("index"))
        except ValueError as exc:
            flash(str(exc), "error")
    return render_template("student_form.html", student=student)

@app.route("/students/<student_id>/delete", methods=["POST"])
def delete_student(student_id):
    students = records()
    student = find_student(student_id, students)
    students.remove(student)
    save_students(students, DATA_FILE)
    flash("Student record deleted.", "success")
    return redirect(url_for("index"))

@app.route("/students/<student_id>/scores", methods=["GET", "POST"])
def scores(student_id):
    students = records()
    student = find_student(student_id, students)
    if request.method == "POST":
        try:
            new_scores = {}
            for subject in SUBJECTS:
                score = float(request.form.get(subject, ""))
                if not 0 <= score <= 100:
                    raise ValueError
                new_scores[subject] = score
            student.scores = new_scores
            student.result_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_students(students, DATA_FILE)
            flash("Scores saved successfully.", "success")
            return redirect(url_for("report", student_id=student_id))
        except (ValueError, TypeError):
            flash("Enter a valid score from 0 to 100 for every subject.", "error")
    return render_template("scores.html", student=student, subjects=SUBJECTS)

@app.route("/students/<student_id>")
def report(student_id):
    student = find_student(student_id, records())
    return render_template("report.html", student=student)

@app.errorhandler(404)
def missing(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
