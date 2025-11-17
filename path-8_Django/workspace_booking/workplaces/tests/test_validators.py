from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from employees.models import EmployeeProfile, EmployeeSkill, Skill
from workplaces.models import Workplace


class WorkplaceValidatorTests(TestCase):
    """Тесты для валидатора рабочих мест"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Создаем навыки
        self.backend_skill = Skill.objects.create(name="Бэкенд")
        self.frontend_skill = Skill.objects.create(name="Фронтэнд")
        self.testing_skill = Skill.objects.create(name="Тестирование")
        self.design_skill = Skill.objects.create(name="Дизайн")

        # Создаем пользователей и сотрудников
        self.dev_user = User.objects.create_user(
            username="developer", password="testpass"
        )
        self.tester_user = User.objects.create_user(
            username="tester", password="testpass"
        )
        self.designer_user = User.objects.create_user(
            username="designer", password="testpass"
        )

        self.developer = EmployeeProfile.objects.create(
            user=self.dev_user,
            first_name="Разработчик",
            last_name="Тестовый",
            gender="M",
        )
        # Исправляем: создаем связь через EmployeeSkill с указанием уровня
        EmployeeSkill.objects.create(
            employee=self.developer, skill=self.backend_skill, level=8
        )

        self.tester = EmployeeProfile.objects.create(
            user=self.tester_user,
            first_name="Тестировщик",
            last_name="Тестовый",
            gender="F",
        )
        EmployeeSkill.objects.create(
            employee=self.tester, skill=self.testing_skill, level=7
        )

        self.designer = EmployeeProfile.objects.create(
            user=self.designer_user,
            first_name="Дизайнер",
            last_name="Тестовый",
            gender="M",
        )
        EmployeeSkill.objects.create(
            employee=self.designer, skill=self.design_skill, level=9
        )

    def test_developer_cannot_sit_next_to_tester(self):
        """Тест: разработчик не может сидеть рядом с тестировщиком"""
        # Создаем рабочие места
        workplace1 = Workplace.objects.create(table_number=1, employee=self.tester)
        workplace2 = Workplace.objects.create(table_number=2)

        # Пытаемся посадить разработчика рядом с тестировщиком
        workplace2.employee = self.developer

        # Должна возникнуть ошибка валидации
        with self.assertRaises(ValidationError):
            workplace2.full_clean()

    def test_tester_cannot_sit_next_to_developer(self):
        """Тест: тестировщик не может сидеть рядом с разработчиком"""
        # Создаем рабочие места
        workplace1 = Workplace.objects.create(table_number=1, employee=self.developer)
        workplace2 = Workplace.objects.create(table_number=2)

        # Пытаемся посадить тестировщика рядом с разработчиком
        workplace2.employee = self.tester

        # Должна возникнуть ошибка валидации
        with self.assertRaises(ValidationError):
            workplace2.full_clean()

    def test_non_tech_employees_can_sit_together(self):
        """Тест: нетекстовые сотрудники могут сидеть рядом"""
        # Создаем второго дизайнера
        designer2_user = User.objects.create_user(
            username="designer2", password="testpass"
        )
        designer2 = EmployeeProfile.objects.create(
            user=designer2_user, first_name="Дизайнер", last_name="Второй", gender="F"
        )
        EmployeeSkill.objects.create(
            employee=designer2, skill=self.design_skill, level=8
        )

        workplace1 = Workplace.objects.create(table_number=1, employee=self.designer)
        workplace2 = Workplace.objects.create(table_number=2, employee=designer2)

        # Не должно быть ошибки валидации
        try:
            workplace1.full_clean()
            workplace2.full_clean()
        except ValidationError:
            self.fail("Дизайнеры должны иметь возможность сидеть рядом!")
