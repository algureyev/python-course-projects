from django.db import models
from django.core.validators import MinValueValidator
from employees.models import EmployeeProfile
from .validators import validate_developer_tester_neighbors

class Workplace(models.Model):
    table_number = models.IntegerField(
        unique=True, 
        verbose_name='Номер стола',
        validators=[MinValueValidator(1)]
    )
    employee = models.OneToOneField(
        EmployeeProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Закрепленный сотрудник'
    )
    additional_info = models.TextField(blank=True, verbose_name='Дополнительная информация')
    
    def clean(self):
        """Валидация при сохранении"""
        super().clean()
        validate_developer_tester_neighbors(self)
    
    def save(self, *args, **kwargs):
        """Переопределяем save для вызова валидации"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Стол {self.table_number}"
    
    class Meta:
        verbose_name = 'Рабочее место'
        verbose_name_plural = 'Рабочие места'