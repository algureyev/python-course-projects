import django_filters

from .models import EmployeeProfile


class EmployeeFilter(django_filters.FilterSet):
    min_experience = django_filters.NumberFilter(
        method="filter_min_experience", label="Минимальный стаж (дни)"
    )
    max_experience = django_filters.NumberFilter(
        method="filter_max_experience", label="Максимальный стаж (дни)"
    )
    skills = django_filters.CharFilter(
        method="filter_skills", label="Навыки (поиск по названию)"
    )
    skill_ids = django_filters.ModelMultipleChoiceFilter(
        field_name="skills__id",
        queryset=lambda request: EmployeeProfile.objects.none(),
        label="Навыки (по ID)",
    )

    class Meta:
        model = EmployeeProfile
        fields = {
            "first_name": ["icontains", "exact"],
            "last_name": ["icontains", "exact"],
            "gender": ["exact"],
            "hire_date": ["exact", "gte", "lte"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Динамически устанавливаем queryset для skill_ids
        from .models import Skill

        self.filters["skill_ids"].extra["queryset"] = Skill.objects.all()

    def filter_min_experience(self, queryset, name, value):
        """
        Фильтр по минимальному стажу
        """
        from datetime import date, timedelta

        try:
            min_date = date.today() - timedelta(days=int(value))
            return queryset.filter(hire_date__lte=min_date)
        except (ValueError, TypeError):
            return queryset

    def filter_max_experience(self, queryset, name, value):
        """
        Фильтр по максимальному стажу
        """
        from datetime import date, timedelta

        try:
            max_date = date.today() - timedelta(days=int(value))
            return queryset.filter(hire_date__gte=max_date)
        except (ValueError, TypeError):
            return queryset

    def filter_skills(self, queryset, name, value):
        """
        Кастомный фильтр по навыкам
        """
        return queryset.filter(skills__name__icontains=value).distinct()
