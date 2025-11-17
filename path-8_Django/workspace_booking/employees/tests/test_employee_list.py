from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from employees.models import EmployeeProfile


class EmployeeListViewTests(TestCase):
    """Тесты для списка пользователей (K2)"""

    def setUp(self):
        # Создаем несколько сотрудников для пагинации
        for i in range(15):
            user = User.objects.create_user(username=f"user{i}", password="testpass")
            employee = EmployeeProfile.objects.create(
                user=user,
                first_name=f"Имя{i}",
                last_name=f"Фамилия{i}",
                gender="M" if i % 2 == 0 else "F",
                hire_date=date.today() - timedelta(days=i * 10),
            )

    def test_employee_list_status_code(self):
        """K2: Проверка доступности списка сотрудников"""
        response = self.client.get(reverse("employees:employee_list"))
        self.assertEqual(response.status_code, 200)

    def test_employee_list_template(self):
        """K2: Проверка использования правильного шаблона"""
        response = self.client.get(reverse("employees:employee_list"))
        self.assertTemplateUsed(response, "employees/employee_list.html")

    def test_employee_list_context(self):
        """K2: Проверка контекста списка сотрудников"""
        response = self.client.get(reverse("employees:employee_list"))
        self.assertIn("employees", response.context)
        self.assertIn("page_obj", response.context)

    def test_employee_list_pagination(self):
        """K2: Проверка пагинации (10 сотрудников на страницу)"""
        response = self.client.get(reverse("employees:employee_list"))
        self.assertEqual(len(response.context["employees"]), 10)  # paginate_by = 10

        # Проверяем вторую страницу
        response = self.client.get(reverse("employees:employee_list") + "?page=2")
        self.assertEqual(
            len(response.context["employees"]), 5
        )  # осталось 5 сотрудников

    def test_employee_list_ordering(self):
        """K2: Проверка сортировки по дате приема (новые первыми)"""
        response = self.client.get(reverse("employees:employee_list"))
        employees = response.context["employees"]

        # Проверяем что сотрудники отсортированы по убыванию даты приема
        hire_dates = [emp.hire_date for emp in employees]
        self.assertEqual(hire_dates, sorted(hire_dates, reverse=True))
