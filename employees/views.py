from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Employee
from .serializers import EmployeeSerializer
from mongoengine.errors import NotUniqueError, DoesNotExist

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5  # number of employees per page
    page_size_query_param = 'page_size'
    max_page_size = 50

class EmployeeViewSet(viewsets.ViewSet):
    """
    Employee CRUD, Querying & Aggregation API using MongoEngine
    """
    permission_classes = [IsAuthenticated]  # JWT-protected routes
    pagination_class = StandardResultsSetPagination

    # List all employees or filter by department with pagination
    def list(self, request):
        department = request.query_params.get('department')
        if department:
            employees = Employee.objects(department=department).order_by('-joining_date')
        else:
            employees = Employee.objects().order_by('-joining_date')

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(list(employees), request)
        serializer = EmployeeSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # Create a new employee
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                employee = Employee(**serializer.validated_data)
                employee.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except NotUniqueError:
                return Response({"error": "Employee ID must be unique."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve employee by employee_id
    def retrieve(self, request, pk=None):
        try:
            employee = Employee.objects.get(employee_id=pk)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except DoesNotExist:
            return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # Update employee (partial updates allowed)
    def update(self, request, pk=None):
        try:
            employee = Employee.objects.get(employee_id=pk)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                for key, value in serializer.validated_data.items():
                    setattr(employee, key, value)
                employee.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DoesNotExist:
            return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # Delete employee
    def destroy(self, request, pk=None):
        try:
            employee = Employee.objects.get(employee_id=pk)
            employee.delete()
            return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except DoesNotExist:
            return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # Average salary by department
    @action(detail=False, methods=['get'])
    def avg_salary(self, request):
        pipeline = [
            {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}}
        ]
        result = Employee.objects.aggregate(*pipeline)
        data = [{"department": r["_id"], "avg_salary": r["avg_salary"]} for r in result]
        return Response(data)

    # Search employees by skill
    @action(detail=False, methods=['get'])
    def search(self, request):
        skill = request.query_params.get('skill')
        if not skill:
            return Response({"error": "Skill query parameter required."}, status=status.HTTP_400_BAD_REQUEST)
        employees = Employee.objects(skills=skill)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
