from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from .models import EmployeeProfile

class HomeView(ListView):
    model = EmployeeProfile
    template_name = 'employees/home.html'
    context_object_name = 'employees'
    
    def get_queryset(self):
        return EmployeeProfile.objects.prefetch_related(
            'employeeskill_set__skill',
            'images'
        ).order_by('-hire_date')[:4]  # 4 последних нанятых сотрудника

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Общее количество сотрудников
        context['total_employees'] = EmployeeProfile.objects.count()
        return context

class EmployeeListView(ListView):
    model = EmployeeProfile
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10  # Пагинация по 10 сотрудников

    def get_queryset(self):
        # Оптимизация: prefetch_related для навыков и изображений
        return EmployeeProfile.objects.prefetch_related(
            'employeeskill_set__skill',
            'images'
        ).order_by('-hire_date')

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'
    login_url = '/admin/login/'

    def get_queryset(self):
        # Оптимизация: prefetch_related для навыков, изображений и рабочего места
        return EmployeeProfile.objects.prefetch_related(
            'employeeskill_set__skill',
            'images'
        ).select_related('workplace')