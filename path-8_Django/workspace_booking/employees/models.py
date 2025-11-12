from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название навыка')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

class EmployeeProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    skills = models.ManyToManyField(Skill, through='EmployeeSkill', verbose_name='Навыки')
    description = RichTextField(verbose_name='Описание', blank=True)
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    class Meta:
        verbose_name = 'Профиль сотрудника'
        verbose_name_plural = 'Профили сотрудников'

class EmployeeSkill(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        verbose_name='Уровень навыка'
    )
    
    class Meta:
        verbose_name = 'Навык сотрудника'
        verbose_name_plural = 'Навыки сотрудников'