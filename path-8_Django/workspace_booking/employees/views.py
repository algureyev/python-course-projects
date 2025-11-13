from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EmployeeProfile

class HomeView(ListView):
    model = EmployeeProfile
    template_name = 'employees/home.html'
    context_object_name = 'employees'
    
    def get_queryset(self):
        return EmployeeProfile.objects.all()[:6]  # Показываем первые 6 сотрудников на главной

class EmployeeListView(ListView):
    model = EmployeeProfile
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'
    login_url = '/admin/login/'