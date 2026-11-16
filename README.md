# Student Result Management System

A Python project containing a command-line program and a browser-based web interface built with Flask.

## Features
- Register, view, search (terminal version), update and delete student records.
- Record scores in Mathematics, English, Physics, Chemistry and Biology.
- Calculate total scores, averages and grades.
- View individual report cards and class performance statistics.
- Store student records in JSON.

## Run the command-line version
Run `python main.py` from this folder.

## Run the web version locally
1. Install Python 3.9 or later.
2. Run `pip install -r requirements.txt`.
3. Run `python app.py`.
4. Open `http://127.0.0.1:5000` in your browser.

## Deploy on Render
See `RENDER_DEPLOYMENT.md`. Render build command: `pip install -r requirements.txt`. Start command: `gunicorn app:app`.

## Data persistence notice
The sample app stores data in `data/students.json`. Free hosting filesystems may be temporary, so records may be lost after restarts or redeployments. Do not use it for real student records without adding persistent database storage.

## Concepts demonstrated
Variables, data types, conditionals, loops, lists, dictionaries, functions, classes, sorting, exception handling, JSON file handling, modules, date/time handling, Flask routes and HTML templates.
