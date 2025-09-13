from rest_framework import serializers
from .models import Employee
from datetime import date

class EmployeeSerializer(serializers.Serializer):
    employee_id = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=100)
    department = serializers.CharField(max_length=100)
    salary = serializers.FloatField()
    joining_date = serializers.DateField()
    skills = serializers.ListField(
        child=serializers.CharField(max_length=50)
    )

    def validate_salary(self, value):
        """Ensure salary is positive."""
        if value < 0:
            raise serializers.ValidationError("Salary must be positive.")
        return value

    def validate_joining_date(self, value):
        """Ensure joining date is not in the future."""
        if value > date.today():
            raise serializers.ValidationError("Joining date cannot be in the future.")
        return value

    def create(self, validated_data):
        """Create a new Employee document in MongoDB."""
        from .models import Employee
        employee = Employee(**validated_data)
        employee.save()
        return employee

    def update(self, instance, validated_data):
        """Update an existing Employee document."""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
