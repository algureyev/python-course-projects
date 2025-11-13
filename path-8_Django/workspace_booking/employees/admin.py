from django.contrib import admin
from .models import Skill, EmployeeProfile, EmployeeSkill, EmployeeImage

class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1
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
admin.site.register(EmployeeImage)