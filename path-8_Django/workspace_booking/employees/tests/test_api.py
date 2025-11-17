from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from employees.models import EmployeeProfile, EmployeeSkill, Skill
from workplaces.models import Workplace


class EmployeeAPITests(APITestCase):
    """
    Тесты для API сотрудников
    """

    def setUp(self):
        # Создаем тестовых пользователей
        self.visitor = User.objects.create_user(
            username="visitor", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin", password="adminpass123", is_staff=True
        )

        # Создаем тестовые данные
        self.skill = Skill.objects.create(name="Python")
        self.workplace = Workplace.objects.create(table_number=1)

        self.employee = EmployeeProfile.objects.create(
            user=User.objects.create_user("emp_user", "emppass123"),
            first_name="Тест",
            last_name="Сотрудник",
            gender="M",
        )
        EmployeeSkill.objects.create(employee=self.employee, skill=self.skill, level=8)

        # API клиенты
        self.visitor_client = APIClient()
        self.admin_client = APIClient()

        # Аутентифицируем клиентов
        self.visitor_client.force_authenticate(user=self.visitor)
        self.admin_client.force_authenticate(user=self.admin)

    def test_get_employees_list_authenticated(self):
        """K2: Аутентифицированный пользователь может получить список сотрудников"""
        response = self.visitor_client.get("/api/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_get_employees_list_unauthenticated(self):
        """Неаутентифицированный пользователь не может получить список"""
        client = APIClient()  # Неаутентифицированный клиент
        response = client.get("/api/employees/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_employees_by_skills(self):
        """K3: Фильтрация сотрудников по навыкам"""
        response = self.visitor_client.get("/api/employees/?skills=Python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_admin_can_create_employee(self):
        """K4: Администратор может создавать сотрудников"""
        data = {
            "first_name": "Новый",
            "last_name": "Сотрудник",
            "gender": "F",
        }
        response = self.admin_client.post("/api/employees/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_visitor_cannot_create_employee(self):
        """K4: Посетитель не может создавать сотрудников"""
        data = {
            "first_name": "Новый",
            "last_name": "Сотрудник",
            "gender": "F",
        }
        response = self.visitor_client.post("/api/employees/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_jwt_authentication(self):
        """K5: JWT аутентификация работает"""
        # Тест получения токена
        client = APIClient()
        response = client.post(
            "/api/token/", {"username": "visitor", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
