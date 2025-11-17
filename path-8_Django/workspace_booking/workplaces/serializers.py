from rest_framework import serializers

from employees.serializers import EmployeeProfileSerializer

from .models import Workplace


class WorkplaceSerializer(serializers.ModelSerializer):
    employee_info = EmployeeProfileSerializer(source="employee", read_only=True)

    class Meta:
        model = Workplace
        fields = ["id", "table_number", "employee", "employee_info", "additional_info"]
        read_only_fields = ["id"]
