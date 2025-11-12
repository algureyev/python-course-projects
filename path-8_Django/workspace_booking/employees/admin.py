from django.contrib import admin
from .models import Skill, EmployeeProfile, EmployeeSkill

class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'gender']
    inlines = [EmployeeSkillInline]

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(EmployeeSkill)