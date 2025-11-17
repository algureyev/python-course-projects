from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from employees.models import EmployeeProfile, EmployeeSkill, Skill


class HomePageTests(TestCase):
    """Тесты для главной страницы (K1)"""

    def setUp(self):
        # Создаем тестовых сотрудников
        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")

        self.employee1 = EmployeeProfile.objects.create(
            user=self.user1,
            first_name="Иван",
            last_name="Иванов",
            gender="M",
            hire_date=date.today() - timedelta(days=30),  # Стаж 30 дней
        )

        self.employee2 = EmployeeProfile.objects.create(
            user=self.user2,
            first_name="Мария",
            last_name="Петрова",
            gender="F",
            hire_date=date.today() - timedelta(days=15),  # Стаж 15 дней
        )

        # Добавляем навыки
        skill_python = Skill.objects.create(name="Python")
        skill_testing = Skill.objects.create(name="Тестирование")

        EmployeeSkill.objects.create(
            employee=self.employee1, skill=skill_python, level=8
        )
        EmployeeSkill.objects.create(
            employee=self.employee2, skill=skill_testing, level=7
        )

    def test_home_page_status_code(self):
        """K1: Проверка доступности главной страницы"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """K1: Проверка использования правильного шаблона"""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "employees/home.html")

    def test_home_page_context_employees(self):
        """K1: Проверка контекста - новые сотрудники"""
        response = self.client.get(reverse("home"))
        self.assertIn("employees", response.context)
        # Должны отображаться 2 последних сотрудника
        self.assertEqual(len(response.context["employees"]), 2)

    def test_home_page_context_total_employees(self):
        """K1: Проверка контекста - общее количество сотрудников"""
        response = self.client.get(reverse("home"))
        self.assertIn("total_employees", response.context)
        self.assertEqual(response.context["total_employees"], 2)

    def test_home_page_shows_new_employees(self):
        """K1: Проверка что на главной отображаются новые сотрудники"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Иван Иванов")
        self.assertContains(response, "Мария Петрова")
