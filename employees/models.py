from mongoengine import Document, StringField, FloatField, DateField, ListField, ValidationError
from datetime import datetime

def validate_salary(value):
    if value < 0:
        raise ValidationError("Salary cannot be negative.")

class Employee(Document):
    employee_id = StringField(required=True, unique=True, max_length=20)
    name = StringField(required=True, max_length=100)
    department = StringField(required=True, max_length=100)
    salary = FloatField(required=True, validation=validate_salary)
    joining_date = DateField(required=True)
    skills = ListField(StringField(max_length=50))

    meta = {
        'collection': 'employees',  # MongoDB collection name
        'indexes': [
            'employee_id',            # index for fast lookup
            'department',             # index to filter by department
            'skills',                 # index for skill searches
        ]
    }

    def to_json(self):
        """Convert Employee document to JSON serializable format."""
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "department": self.department,
            "salary": self.salary,
            "joining_date": self.joining_date.strftime("%Y-%m-%d"),
            "skills": self.skills,
        }

    def clean(self):
        """Schema validation for Employee document."""
        # Ensure salary is positive
        if self.salary < 0:
            raise ValidationError("Salary must be positive.")

        # Ensure joining_date is not in the future
        if self.joining_date > datetime.now().date():
            raise ValidationError("Joining date cannot be in the future.")

        # Ensure employee_id is not empty
        if not self.employee_id:
            raise ValidationError("Employee ID is required.")

        # Ensure name is not empty
        if not self.name:
            raise ValidationError("Employee name is required.")
