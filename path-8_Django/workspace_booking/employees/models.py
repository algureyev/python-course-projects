import os
from datetime import date

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название навыка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"


class EmployeeProfile(models.Model):
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    skills = models.ManyToManyField(
        Skill, through="EmployeeSkill", verbose_name="Навыки"
    )
    description = RichTextField(verbose_name="Описание", blank=True)
    hire_date = models.DateField(
        verbose_name="Дата приёма на работу", default=date.today
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def work_experience_days(self):
        """Стаж работы в днях"""
        return (date.today() - self.hire_date).days

    def get_first_image(self):
        """Получить первое изображение из галереи"""
        return self.images.first()

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)], verbose_name="Уровень навыка"
    )

    class Meta:
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"


class EmployeeImage(models.Model):
    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Сотрудник",
    )
    image = models.ImageField(upload_to="employee_images/", verbose_name="Изображение")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядковый номер")

    class Meta:
        verbose_name = "Изображение сотрудника"
        verbose_name_plural = "Изображения сотрудников"
        ordering = ["order"]

    def __str__(self):
        return f"Изображение {self.order} для {self.employee}"

    def delete(self, *args, **kwargs):
        # Удаляем файл с диска при удалении записи
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
