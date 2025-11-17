from django.test import TestCase
from django.urls import reverse


class EmployeeURLTests(TestCase):
    """Тесты для проверки URL-адресов приложения employees"""

    def test_employee_list_url_exists(self):
        """Проверка доступности списка сотрудников"""
        response = self.client.get(reverse("employees:employee_list"))
        self.assertEqual(response.status_code, 200)

    def test_employee_list_url_accessible_by_name(self):
        """Проверка корректности имени URL для списка сотрудников"""
        url = reverse("employees:employee_list")
        self.assertEqual(url, "/employees/")
