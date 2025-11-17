from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from employees.models import EmployeeProfile, Skill


class EmployeeViewTests(TestCase):
    """Тесты для проверки представлений сотрудников"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        # Создаем тестовые навыки
        self.skill1 = Skill.objects.create(name="Python")
        self.skill2 = Skill.objects.create(name="Тестирование")

        # Создаем тестового сотрудника
        self.employee = EmployeeProfile.objects.create(
            user=self.user, first_name="Иван", last_name="Петров", gender="M"
        )

    def test_employee_list_view_uses_correct_template(self):
        """Проверка использования правильного шаблона"""
        response = self.client.get(reverse("employees:employee_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_list.html")

    def test_employee_list_view_returns_correct_context(self):
        """Проверка корректности контекста"""
        response = self.client.get(reverse("employees:employee_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("employees", response.context)
        self.assertIn("page_obj", response.context)
