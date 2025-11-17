from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from employees.models import EmployeeProfile


class EmployeeAccessTests(TestCase):
    """Тесты для проверки прав доступа (K3, K4)"""

    def setUp(self):
        # Создаем тестовых пользователей
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@test.com"
        )

        # Создаем тестовых сотрудников
        self.employee1 = EmployeeProfile.objects.create(
            user=self.user1, first_name="Иван", last_name="Иванов", gender="M"
        )

        self.employee2 = EmployeeProfile.objects.create(
            user=self.user2, first_name="Мария", last_name="Петрова", gender="F"
        )

    def test_employee_detail_requires_login_anonymous(self):
        """K3, K4: Анонимный пользователь перенаправляется на логин"""
        url = reverse("employees:employee_detail", args=[self.employee1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)  # Редирект
        self.assertIn("/admin/login/", response.url)  # На страницу логина Django

    def test_employee_detail_accessible_with_login(self):
        """K3, K4: Авторизованный пользователь имеет доступ"""
        self.client.login(username="user1", password="testpass123")
        url = reverse("employees:employee_detail", args=[self.employee1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_detail.html")

    def test_employee_detail_context(self):
        """K3, K4: Проверка контекста страницы деталей"""
        self.client.login(username="user1", password="testpass123")
        url = reverse("employees:employee_detail", args=[self.employee1.pk])
        response = self.client.get(url)

        self.assertIn("employee", response.context)
        self.assertEqual(response.context["employee"], self.employee1)

    def test_employee_detail_shows_correct_info(self):
        """K3, K4: Проверка отображения информации о сотруднике"""
        self.client.login(username="user1", password="testpass123")
        url = reverse("employees:employee_detail", args=[self.employee1.pk])
        response = self.client.get(url)

        self.assertContains(response, "Иван Иванов")
        self.assertContains(response, "Мужской")
        self.assertContains(response, "Стаж работы:")

    def test_multiple_employees_accessible(self):
        """K3, K4: Проверка доступа к разным сотрудникам"""
        self.client.login(username="user1", password="testpass123")

        # Проверяем доступ к первому сотруднику
        url1 = reverse("employees:employee_detail", args=[self.employee1.pk])
        response1 = self.client.get(url1)
        self.assertEqual(response1.status_code, 200)

        # Проверяем доступ ко второму сотруднику
        url2 = reverse("employees:employee_detail", args=[self.employee2.pk])
        response2 = self.client.get(url2)
        self.assertEqual(response2.status_code, 200)
