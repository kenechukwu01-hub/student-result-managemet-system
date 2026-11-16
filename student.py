"""Student model and validation."""
from datetime import datetime, date


class Student:
    """Represents one student and the student's subject scores."""

    def __init__(self, student_id, full_name, class_form, gender, date_of_birth,
                 scores=None, result_date=None):
        self.student_id = self._required(student_id, "Student ID")
        self.full_name = self._required(full_name, "Full name")
        self.class_form = self._required(class_form, "Class/Form")
        self.gender = self._required(gender, "Gender")
        self.date_of_birth = self._validate_date(date_of_birth)
        self.scores = scores or {}
        self.result_date = result_date
        self._validate_scores(self.scores)

    @staticmethod
    def _required(value, label):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{label} is required.")
        return value

    @staticmethod
    def _validate_date(value):
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d").date()
            if parsed > date.today():
                raise ValueError("Date of birth cannot be in the future.")
            return parsed.isoformat()
        except (TypeError, ValueError) as error:
            raise ValueError("Date of birth must be a valid date in YYYY-MM-DD format.") from error

    @staticmethod
    def _validate_scores(scores):
        if not isinstance(scores, dict):
            raise ValueError("Scores must be stored as a dictionary.")
        for subject, score in scores.items():
            if not str(subject).strip():
                raise ValueError("Subject name cannot be empty.")
            try:
                number = float(score)
            except (TypeError, ValueError) as error:
                raise ValueError(f"Score for {subject} must be numeric.") from error
            if not 0 <= number <= 100:
                raise ValueError(f"Score for {subject} must be between 0 and 100.")

    def update_details(self, full_name, class_form, gender, date_of_birth):
        self.full_name = self._required(full_name, "Full name")
        self.class_form = self._required(class_form, "Class/Form")
        self.gender = self._required(gender, "Gender")
        self.date_of_birth = self._validate_date(date_of_birth)

    @property
    def total(self):
        return sum(float(score) for score in self.scores.values())

    @property
    def average(self):
        return self.total / len(self.scores) if self.scores else 0.0

    @property
    def grade(self):
        from results import calculate_grade
        return calculate_grade(self.average) if self.scores else "N/A"

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "class_form": self.class_form,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "scores": self.scores,
            "result_date": self.result_date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["student_id"], data["full_name"], data["class_form"],
            data["gender"], data["date_of_birth"], data.get("scores", {}),
            data.get("result_date")
        )

    def __str__(self):
        return (f"{self.student_id} | {self.full_name} | {self.class_form} | "
                f"{self.gender} | DOB: {self.date_of_birth}")
