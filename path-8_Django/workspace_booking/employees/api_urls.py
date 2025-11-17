from django.urls import include, path
from rest_framework.routers import DefaultRouter

from workplaces.api_views import WorkplaceViewSet

from .api_views import (EmployeeImageViewSet, EmployeeSkillViewSet,
                        EmployeeViewSet)

# Создаем router для автоматической генерации URL
router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"employee-skills", EmployeeSkillViewSet, basename="employee-skill")
router.register(r"employee-images", EmployeeImageViewSet, basename="employee-image")
router.register(r"workplaces", WorkplaceViewSet, basename="workplace")

urlpatterns = [
    path("", include(router.urls)),
]
