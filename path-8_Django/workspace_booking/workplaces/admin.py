from django import forms
from django.contrib import admin

from .models import Workplace
from .validators import validate_developer_tester_neighbors


class WorkplaceForm(forms.ModelForm):
    class Meta:
        model = Workplace
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        validate_developer_tester_neighbors(self.instance)
        return cleaned_data


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    form = WorkplaceForm
    list_display = ["table_number", "employee"]
    list_filter = ["table_number"]
    search_fields = ["table_number", "employee__first_name", "employee__last_name"]
